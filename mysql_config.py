import mysql.connector
from pymongo import MongoClient
from mongodb import *

class MySQLDB:

  def __init__(self):
      self.db = mysql.connector.connect(
          host="localhost",
          user="root",
          password="Rahane@27"
      )

      self.cursor = self.db.cursor()

      # Check if the database exists
      self.cursor.execute("SHOW DATABASES") 
      existing_databases = [db[0] for db in self.cursor]

      if "youtube_db" not in existing_databases:
          self.cursor.execute("CREATE DATABASE Youtube_DB")
      else:
          print("Database already exists")

      self.db = mysql.connector.connect(
          host="localhost",
          user="root",
          password="Rahane@27",
          database="Youtube_DB"
      )

      self.cursor = self.db.cursor()

      # Connect to MongoDB
      client = MongoClient('mongodb+srv://naveenkumaragnitiosystems:hhq07Xc3BHw0YJe8@cluster0.ndgbb6t.mongodb.net/')
      self.mongodb = client["youtube_db"]


  def insert_channel_table(self):

    cursor = self.cursor

    query = """CREATE TABLE IF NOT EXISTS Channels (
      channel_id varchar(255) PRIMARY KEY, 
      channel_name varchar(255),
      channel_type varchar(255),
      channel_views int,
      channel_description text,
      channel_status varchar(50)
    )"""

    cursor.execute(query) 

    print("Channels Table created")

    channel_col = list(self.mongodb['channels'].find())

    for channel in channel_col:

      id = channel.get('Channel ID')
      name = channel.get('Channel Name')
      type = channel.get('Channel Type')
      views = channel.get('Channel Views')
      status = channel.get('Channel Status')
      description = channel.get('Channel Description')
      insert_query = "INSERT IGNORE INTO channels (channel_id, channel_name, channel_type, channel_views, channel_description, channel_status) VALUES (%s, %s, %s, %s, %s, %s)"
      data=(id,name,type,views,description,status)
      cursor.execute(insert_query, data)
      # Commit the changes to the database
      self.db.commit()
      print("Data inserted successfully.")
   


  def insert_playlist_table(self):

    cursor = self.cursor
    query="""CREATE TABLE IF NOT EXISTS Playlist (
      playlist_id varchar(255) PRIMARY KEY,
      channel_id  varchar(255), 
      playlist_name varchar(255),
      FOREIGN KEY (channel_id) REFERENCES Channels(channel_id)
    )
    """
    cursor.execute(query) 

    print("Playlist Table created")


    # SQL query to insert data into the 'Playlist' table
    insert_query = "INSERT IGNORE INTO Playlist (playlist_id, channel_id, playlist_name) VALUES (%s, %s, %s)"
    playlist_col = self.mongodb['playlists'].find()
    for playlist in playlist_col:
      data = (
              playlist["playlist_id"],
              playlist["playlist_channel_id"],
              playlist["playlist_name"]
          )

        # Execute the SQL query with the data
      cursor.execute(insert_query, data)

      # Commit the changes to the database
      self.db.commit()
    print("Data inserted successfully into the Playlist table.")
  


  def insert_video_table(self):
    cursor = self.cursor

    query = """CREATE TABLE IF NOT EXISTS Videos (
        video_id varchar(255) PRIMARY KEY, 
        playlist_id varchar(255),
        video_name varchar(255),
        video_description text,
        video_published_date datetime,
        views_count int,
        likes_count int, 
        dislikes_count int,
        favorites_count int,
        comments_count int,
        duration int,
        thumbnails varchar(255),
        caption_status varchar(255),
        FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id)
    )
    """
    cursor.execute(query)

    print("Videos Table created")
    insert_query = """
        INSERT IGNORE INTO Videos (video_id, playlist_id, video_name, video_description, video_published_date, views_count,
        likes_count, dislikes_count, favorites_count, comments_count, duration, thumbnails, caption_status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    videos_col = self.mongodb['Videos'].find()

    try:
        for video in videos_col:
            data = (
                video["video_id"],
                video["playlist_id"],
                video["video_name"],
                video["video_description"],
                video["video_published_date"],
                video["views_count"],
                video["likes_count"],
                video["dislikes_count"],
                video["favorites_count"],
                video["comments_count"],
                video["duration"],
                video["thumbnails"],
                video["caption_status"]
            )
            # Execute the SQL query with the data
            cursor.execute(insert_query, data)

        # Commit the changes to the database
        self.db.commit()
        print("Data inserted successfully into the Videos table.")
    except Exception as e:
        print(f"Error inserting data into Videos table: {e}")



  def insert_comments_table(self):

    cursor = self.cursor
    query="""CREATE TABLE IF NOT EXISTS Comments (
    comment_id varchar(255) PRIMARY KEY,
    video_id  varchar(255),
    comment_text text,
    comment_author varchar(255),
    comment_published_date datetime,
    FOREIGN KEY (video_id) REFERENCES Videos(video_id)
    )
    """
    cursor.execute(query) 

    print("Comments Table created")

    insert_query = """
        INSERT IGNORE INTO Comments (comment_id, video_id, comment_text, comment_author, comment_published_date) 
        VALUES (%s, %s, %s, %s, %s)
        """
    Comments_col = self.mongodb['Comments'].find()
    for comment in Comments_col:
      data = (
            comment["comment_id"],
            comment["video_id"],
            comment["comment_text"],
            comment["comment_author"],
            comment["comment_published_date"]
        )
      # Execute the SQL query with the data
      cursor.execute(insert_query, data)

      # Commit the changes to the database
      self.db.commit()
    print("Data inserted successfully into the Comments table.")

    self.db.close()

def display_output(self, question):
  pass
