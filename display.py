import mysql
import pandas as pd


class Display:
    def __init__(self):
      self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Rahane@27",
            database="Youtube_DB"
        )
      
    
    def display_output(self,question):

      if question==0:
          query="""select video_name, c.channel_name from videos v 
                join playlist p on v.playlist_id = p.playlist_id 
                join channels c on p.channel_id = c.channel_id;"""
          engine = self.db
          df = pd.read_sql(query,engine)
          return df
      elif question==1:
          query="""select c.channel_name,count(*) video_count from videos v 
                    join playlist p on v.playlist_id = p.playlist_id 
                    join channels c on p.channel_id = c.channel_id 
                    group by c.channel_id 
                    order by video_count desc 
                    limit 1;"""
          engine = self.db
          df = pd.read_sql(query,engine)
          return df
      elif question==2:
          query="""select c.channel_name,video_name, max(views_count) most_viewed from videos v 
                  join playlist p on v.playlist_id = p.playlist_id 
                  join channels c on p.channel_id = c.channel_id 
                  group by video_id 
                  order by most_viewed desc 
                  limit 10;"""
          engine = self.db
          df = pd.read_sql(query,engine)
          return df
      elif question==3:
          query="""select video_name, comments_count from videos;"""
          engine = self.db
          df = pd.read_sql(query,engine)
          return df
      elif question==4:
          query="""select video_name, c.channel_name, max(likes_count) most_liked from videos v 
                    join playlist p on v.playlist_id = p.playlist_id
                    join channels c on p.channel_id = c.channel_id 
                    group by video_id order by most_liked desc limit 1;"""
          engine = self.db
          df = pd.read_sql(query,engine)
          return df
      elif question==5:
          query="""select video_name,likes_count, dislikes_count from videos;"""
          engine = self.db
          df = pd.read_sql(query,engine)
          return df
      elif question==6:
          query="""select channel_name, channel_views from channels;"""
          engine = self.db
          df = pd.read_sql(query,engine)
          return df
      elif question==7:
          query="""select distinct channel_name from channels c 
                  join playlist p on c.channel_id = p.channel_id 
                  join videos v on p.playlist_id = v.playlist_id where year(v.video_published_date) =2022;"""
          engine = self.db
          df = pd.read_sql(query,engine)
          return df
      elif question==8:
          query="""select c.channel_name,avg(v.duration) video_duration from videos v 
                    join playlist p on v.playlist_id = p.playlist_id 
                    join channels c on p.channel_id = c.channel_id group by c.channel_id;"""
          engine = self.db
          df = pd.read_sql(query,engine)
          return df
      elif question==9:
          query="""select c.channel_name, v.video_name, v.comments_count from videos v 
                  join playlist p on v.playlist_id=p.playlist_id 
                  join channels c on p.channel_id=c.channel_id 
                  order by comments_count desc limit 1;"""
          engine = self.db
          df = pd.read_sql(query,engine)
          return df
      