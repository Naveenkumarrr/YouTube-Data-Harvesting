from isodate import parse_duration
import datetime
from googleapiclient.errors import HttpError
import googleapiclient.discovery as apiclient
import streamlit as st
import requests
import importlib

tab1, tab2 = st.tabs(["Home", "Display"])



# Replace these values with your own credentials and settings
API_KEY = 'AIzaSyB8QccKYXYdlnVZxhPHJ6sQ3aeJYVih-Do'
with tab1:
    st.title('Youtube Harvesting')
    CHANNEL_ID = str(st.text_input("Enter your Channel ID:")).strip()
    isSubmit = st.button('Submit to Harvest')


    # Create a YouTube API client
    youtube = apiclient.build('youtube', 'v3', developerKey=API_KEY)



    class Home:

        def __init__(self):
            self.mdb = importlib.import_module('mongodb').MongoDB()
            

        @staticmethod
        def is_valid_channel_id(channel_id):
            url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"

            response = requests.get(url)

            if response.status_code == 200 and response.json()["pageInfo"]["totalResults"] > 0:
                print(response.status_code)
                return True
            else:
                return False

        def get_channel_info(self):
            # Your implementation...
                # Retrieve channel details
            channel_response = youtube.channels().list(
                part='snippet,statistics,status',
                id=CHANNEL_ID
            ).execute()

            if 'items' not in channel_response:
                print("No channel found.")
                return

            channel_data = channel_response['items'][0]
            channel_id = channel_data['id']
            channel_name = channel_data['snippet']['title']
            channel_type = channel_data['snippet'].get('channelType')
            channel_views = channel_data['statistics']['viewCount']
            channel_status = channel_data.get('status')['privacyStatus']
            channel_description = channel_data['snippet']['description']

            channel_info = {
                "Channel ID": channel_id,
                "Channel Name": channel_name,
                "Channel Type": channel_type,
                "Channel Views": channel_views,
                "Channel Status": channel_status,
                "Channel Description": channel_description
            }

            return channel_info

        def get_all_playlists(self):
            # Your implementation...
                    # Retrieve all playlists from the channel with pagination
            playlists = []
            next_page_token = None

            while True:
                playlist_response = youtube.playlists().list(
                    part='snippet',
                    channelId=CHANNEL_ID,
                    maxResults=50,
                    pageToken=next_page_token
                ).execute()

                if 'items' not in playlist_response:
                    break

                playlists.extend(playlist_response['items'])
                next_page_token = playlist_response.get('nextPageToken')

                if not next_page_token:
                    break

            return playlists
    


        def get_videos_in_playlist(self, playlist_id):
            # Your implementation...
            # Retrieve videos in a playlist
            playlist_items = []
            next_page_token = None

            while True:
                playlist_response = youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=playlist_id,
                    maxResults=200,
                    pageToken=next_page_token
                ).execute()

                playlist_items.extend(playlist_response['items'])
                #print(playlist_items)
                next_page_token = playlist_response.get('nextPageToken')
                #print(next_page_token)

                if not next_page_token:
                    break

            return playlist_items

        def get_video_details(self):
            playlists = self.get_all_playlists()
            videos_lst = []
            playlist_lst = []

            for playlist in playlists[:5]:
                playlist_info = {}
                playlist_id = playlist['id']
                playlist_info['playlist_id'] = playlist_id
                playlist_name = playlist['snippet']['title']
                playlist_info['playlist_name'] = playlist_name
                playlist_info['playlist_channel_id'] = playlist['snippet']['channelId']
                videos = self.get_videos_in_playlist(playlist_id)
                playlist_lst.append(playlist_info)

                if not videos:
                    print(f"No videos found in playlist: {playlist_name}")
                    continue

                for video in videos:
                    video_info = {}
                    video_id = video['snippet']['resourceId']['videoId']
                    video_info['video_id'] = video_id
                    video_info['playlist_id'] = playlist_id

                    video_info['video_name'] = video['snippet']['title']
                    video_info['video_description'] = video['snippet']['description']
                    video_published_date = video['snippet']['publishedAt']
                    video_info['video_published_date'] = datetime.datetime.strptime(video_published_date,
                                                                                    '%Y-%m-%dT%H:%M:%SZ')

                    video_response = youtube.videos().list(
                        part='statistics,contentDetails,statistics',
                        id=video_id
                    ).execute()

                    if 'items' not in video_response:
                        print(f"Video {video_id} not accessible.")
                        continue

                    try:
                        video_statistics = video_response['items'][0].get('statistics')
                        video_content_details = video_response['items'][0].get('contentDetails')
                    except:
                        continue

                    video_info['views_count'] = int(video_statistics.get('viewCount', 0))
                    video_info['likes_count'] = int(video_statistics.get('likeCount', 0))
                    video_info['dislikes_count'] = int(video_statistics.get('dislikeCount', 0))
                    video_info['favorites_count'] = int(video_statistics.get('favoriteCount', 0))
                    video_info['comments_count'] = int(video_statistics.get('commentCount', 0))
                    video_duration = parse_duration(video_content_details.get('duration', 0))
                    video_info['duration'] = video_duration.total_seconds()
                    video_info['thumbnails'] = video['snippet']['thumbnails']['high']['url']
                    video_info['caption_status'] = video_content_details.get('caption', False)

                    videos_lst.append(video_info)

            return videos_lst, playlist_lst

        def get_video_comments(self, video_id):
            comments_lst = []
            try:
                next_page_token = None
                while True:
                    comments_response = youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        pageToken=next_page_token,
                        maxResults=100
                    ).execute()

                    for comment in comments_response['items']:
                        comments_lst.append(comment['snippet'])

                    next_page_token = comments_response.get('nextPageToken')

                    if not next_page_token:
                        break

            except HttpError as e:
                pass

            return comments_lst

        def get_comment_details(self, video_ids):
            comments_lst = []
            for id in video_ids:
                comments = self.get_video_comments(id)
                for comment in comments:
                    comment_info = {}
                    comment_info['comment_id'] = comment["topLevelComment"]['id']
                    comment_info['video_id'] = comment["topLevelComment"]['snippet']['videoId']
                    comment_info['comment_text'] = comment["topLevelComment"]['snippet']['textDisplay']
                    comment_info['comment_author'] = comment["topLevelComment"]['snippet']['authorDisplayName']
                    comment_published_date = comment["topLevelComment"]['snippet']['publishedAt']
                    comment_info['comment_published_date'] = datetime.datetime.strptime(comment_published_date,
                                                                                        '%Y-%m-%dT%H:%M:%SZ')
                    comments_lst.append(comment_info)
            return comments_lst

        def run_app(self):
            if isSubmit:
                youtube_instance = Home()
                if self.is_valid_channel_id(CHANNEL_ID):
                    if youtube_instance.mdb.isChannelexistsAlready(CHANNEL_ID):
                        st.warning('Channel exists already!')
                    else:
                        print("The channel ID : {} is valid.".format(CHANNEL_ID))
                        # Create spinner
                        with st.spinner('Downloading Data...'):
                            channels = self.get_channel_info()
                            videos, playlists = self.get_video_details()
                            video_ids = [id['video_id'] for id in videos]
                            comments = self.get_comment_details(video_ids)
                            youtube_instance.mdb.insert_channel(channels)
                            youtube_instance.mdb.insert_playlist(playlists)
                            youtube_instance.mdb.insert_videos(videos)
                            youtube_instance.mdb.insert_comments(comments)
                        st.success('Data Harvesting is successfully completed!.')
                else:
                    st.warning("The channel ID is invalid.")
                st.stop()

with tab2:

    sql_questions = [
                    '1) Display all videos and corresponding channels',
                    '2) Display channels with the most number of videos',
                    '3) Display the top 10 most viewed videos and channels',
                    '4) Display comments count for each video',
                    '5) Display videos with the most number of likes',
                    '6) Display total number of likes and dislikes',
                    '7) Display total number of views for each channel',
                    '8) Display channels that published videos in 2022',
                    '9) Display average duration of videos for each channel',
                    '10) Display the video with the highest number of comments']
    
    def paginate_data(df, page_number, page_size):
        start_index = (page_number - 1) * page_size
        end_index = min(page_number * page_size, len(df))
        return df[start_index:end_index]
    
    def selected_option(df):
        page_size = 10
        page_number = st.session_state.get('page_number', 1)


        col1, col2, col3 = st.columns(3)
        
        if col1.button('Previous') and page_number > 1:
            page_number -= 1
        col2.write(f'Page {page_number}')
        if col3.button('Next') and page_number < (len(df) // page_size) + 1:
            page_number += 1

        st.session_state.page_number = page_number
        paginated_df = paginate_data(df, page_number, page_size)

        st.table(paginated_df)

    option=st.selectbox(label='Choose an option to view your output:',options=sql_questions,index=None,placeholder="Select an option",)
    if option:
        selected=sql_questions.index(option)
        display = importlib.import_module('display').Display()
        results=display.display_output(selected)
        selected_option(results)

        

# Main block
if __name__ == "__main__":
    youtube_instance = Home()
    youtube_instance.run_app()
