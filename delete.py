
from pymongo import MongoClient
import importlib
import pymongo

client = MongoClient('mongodb+srv://naveenkumaragnitiosystems:hhq07Xc3BHw0YJe8@cluster0.ndgbb6t.mongodb.net/')
db = client["youtube_db"]

channel_col = db["channels"]


channel_col.delete_many({'Channel ID':'UC3qp2FCeaQ5HhA3jHWHbrxg'})