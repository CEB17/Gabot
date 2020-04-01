# Module for MongoDB
import pymongo,os
# Connect to MongoDB Atlas
client = pymongo.MongoClient(f"mongodb+srv://{os.getenv('DB_USER', None)}:{os.getenv('DB_PASSWORD', None)}@cluster0-zh97z.mongodb.net/bot_api?retryWrites=true&w=majority")
db = client['bot_api']