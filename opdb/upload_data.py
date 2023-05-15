import opdb.create_gudata as cg
from pprint import pprint
import pymongo
from pymongo.server_api import ServerApi
import numpy as np
from datetime import datetime


def Upload_User_data():
    times,timeOfDays= cg.numOfData(365)
    Tdata=cg.TrandomdataList(timeOfDays)
    Mdata=cg.MrandomdataList(times)
    Udata=cg.UrandomdataList(times)

    toiletList=[]
    for time in range(times):
        toilet={}
        toilet["timestamp"]=Tdata[time]
        toilet["metadata"]=Mdata[time]
        for udata in Udata[time]:
            for urinalysis in cg.uriaList:
                toilet[urinalysis]=Udata[time][urinalysis]
        toiletList.append(toilet)
    print(toiletList)
    client = pymongo.MongoClient("mongodb+srv://tomcat:cuityjs@cluster0.3ucwlxn.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.health
    col=db.urinedata
    x=col.insert_many(toiletList)
    print(x.inserted_ids)


def Upload_Current_Onedata():
    times=1
    now=datetime.now()
    Tdata=[]
    Tdata.append(datetime(now.year,now.month,now.day,now.hour,now.minute,now.second))
    Mdata=cg.MrandomdataList(times)
    Udata=cg.UrandomdataList(times)
    toilet = {}
    for time in range(times):
        toilet["timestamp"]=Tdata[time]
        toilet["metadata"]=Mdata[time]
        for udata in Udata[time]:
            for urinalysis in cg.uriaList:
                toilet[urinalysis]=Udata[time][urinalysis]
    print(toilet)
    client = pymongo.MongoClient("mongodb+srv://tomcat:cuityjs@cluster0.3ucwlxn.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.health
    col=db.urinedata
    x=col.insert_one(toilet)
    return x
