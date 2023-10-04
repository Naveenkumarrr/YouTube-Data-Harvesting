
from pymongo import MongoClient
import importlib
import pymongo

class MongoDB:
    def __init__(self):
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://naveenkumaragnitiosystems:hhq07Xc3BHw0YJe8@cluster0.ndgbb6t.mongodb.net/')
        self.db = client["youtube_db"]
        self.mysqldb = importlib.import_module('mysql_config').MySQLDB()

    def isChannelexistsAlready(self, id):
        channel_col = self.db["channels"]

        if channel_col.find_one({'Channel ID': id}):
            print('Channel details are existing already!')
            return True
        else:
            return False
        

    def insert_channel(self, channels):
        # Channel collection
        
            channel_col = self.db["channels"]

            if not channel_col.find_one({'Channel ID': channels['Channel ID']}):
                channel_col.insert_one(channels)
                self.mysqldb.insert_channel_table()
                print('Channel details are inserted Successfully!')
            else:
                print('Channel details are existing already!')
        
            

    def insert_playlist(self,playlists):
        # PlayList collection
        playlist_col = self.db["playlists"]  

        try:
            playlist_col.insert_many(playlists)
            self.mysqldb.insert_playlist_table()
            print('Playlist details are inserted Successfully!')
        except pymongo.errors.DuplicateKeyError:
            pass
        except pymongo.errors.BulkWriteError:
            pass
       

    def insert_videos(self,videos):
        # Videos collection
        videos_col = self.db["Videos"]
        try:
            videos_col.insert_many(videos)
            self.mysqldb.insert_video_table()
            print('Videos details are inserted Successfully!')
        except pymongo.errors.DuplicateKeyError:
            pass
        except pymongo.errors.BulkWriteError:
            pass
      

    def insert_comments(self,comments):
        # Videos collection
        comments_col = self.db["Comments"]

        try:
            comments_col.insert_many(comments)
            self.mysqldb.insert_comments_table()
            print('Comments details are inserted Successfully!')
        except pymongo.errors.DuplicateKeyError:
            pass
        except pymongo.errors.BulkWriteError:
            pass
    