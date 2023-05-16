import pymongo
from pymongo.server_api import ServerApi

client = pymongo.MongoClient("mongodb+srv://tomcat:cuityjs@cluster0.3ucwlxn.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.health
FamilyTable = 'Fzhang'
col=db[FamilyTable]