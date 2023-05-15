import pymongo
from pymongo.server_api import ServerApi
import datetime

client = pymongo.MongoClient("mongodb+srv://tomcat:cuityjs@cluster0.3ucwlxn.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db = client.health


'''
starttime=datetime.datetime(2022,1,1,0,0,0)
stoptime=datetime.datetime(2023,1,1,0,0,0)
uid

'''
def Query_Time_Period_Data(username,starttime,stoptime,uid=-1):
    if username =='zhang':
        FamilyTable = 'Fzhang'
    elif username =='wang':
        FamilyTable = 'Fwang'
    else:
        FamilyTable = 'guest'
    col=db[FamilyTable]
    result=[]
    mgQueryStatementdic ={'timestamp': {'$gt':starttime,'$lt':stoptime}}
    if uid!=-1:
        mgQueryStatementdic['metadata'] = {'from': 'toilet-1', 'type': 'urine', 'uid': uid}
    #print(mgQueryStatementdic)
    for cursor in col.find(mgQueryStatementdic):
        result.append(cursor)
    print("result",result)
    return result
    
def Query_Number_of_urination(username,starttime,stoptime,uid=-1): 
    if username =='zhang':
        FamilyTable = 'Fzhang'
    elif username =='wang':
        FamilyTable = 'Fwang'
    else:
        FamilyTable = 'guest'
    col=db[FamilyTable]
    result=[]
    pipeline = [
        {'$match':{
         'timestamp':{'$gt':starttime,'$lt':stoptime},
         'metadata': {'from': 'toilet-1', 'type': 'urine', 'uid': uid}
         }},
        {'$group': {
         '_id':{'$dateToString':{'format':"%Y-%m-%d",'date':"$timestamp"}},
         'count':{ '$sum': 1 }
         }}
        ]
    for cursor in col.aggregate(pipeline):
            result.append(cursor)
    return result

""" starttime=datetime.datetime(2022,1,1,0,0,0)
stoptime=datetime.datetime(2023,1,1,0,0,0)

a=Query_Time_Period_Data(starttime,stoptime,uid=1)
print(a[0])

b=Query_Number_of_urination(starttime,stoptime,uid=1)
print(b[0])
 """