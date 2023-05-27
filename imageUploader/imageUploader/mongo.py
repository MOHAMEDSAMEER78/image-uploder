
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

uri = "mongodb+srv://imageuploderuser:ir2DGLvLRCFKPujW@image-uploader.bioc0kh.mongodb.net/image-uploader-database?retryWrites=true&w=majority"

# Create a new client and connect to the server
MongoDbConnectionClient = MongoClient(uri, tlsCAFile=certifi.where())

try:
    print("Pinging your deployment...")
    MongoDbConnectionClient.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
