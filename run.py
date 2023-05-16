import hashlib

import pymongo
from pymongo.server_api import ServerApi
import uvicorn
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime
# from fastapi.staticfiles import StaticFiles
from utils import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import opdb.inquire_data as opid
import opdb.upload_data as opud

app = FastAPI()
# app.mount('/static', StaticFiles(directory='static'))

# 设置允许跨域请求的源
origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/index')
async def create_user(request: Request):
    # 从request.body中获取数据
    user_data = await request.json()
    # 处理用户数据
    # ...
    # 返回处理结果
    print(user_data)
    return {"message": "User created successfully.", "user": user_data}


class Tolietdata(BaseModel):
    username:Optional[str] # =None
    starttime:datetime=datetime(2022,1,1,0,0,0)
    stoptime:datetime=datetime(2022,2,1,0,0,0)
    uid:Optional[int] # =None


@app.get('/upload')
async def result():
    x=opud.Upload_Current_Onedata()
    print(x)
    return 'ok'


@app.post('/test/')
async def result(data):
    print('data', data)
    return 'ok'


@app.post('/Time_Period_Data/')
async def result(data: Tolietdata):
    print('data', data)
    return jsonable_encoder(opid.Query_Time_Period_Data(data.username,data.starttime, data.stoptime, data.uid))


@app.post('/Time_Period_Data02/')
async def result(request: Request):
    user_data = await request.json()
    print('user_data', user_data)
    # 处理用户数据
    # print('values:', user_data['values']['uid'])
    uid = user_data['values']['uid']
    # start_time = user_data['values']['timeRange'][0]
    # stop_time = user_data['values']['timeRange'][1]
    start_time = datetime.fromisoformat(user_data['values']['timeRange'][0].split(".")[0])
    stop_time = datetime.fromisoformat(user_data['values']['timeRange'][1].split(".")[0])
    # username = user_data['values']['username']
    print(type(start_time))
    print('values:', start_time, stop_time, uid)
    # 返回处理结果
    return jsonable_encoder(opid.Query_Time_Period_Data(start_time, stop_time, uid))


@app.post('/Number_of_urination/')
async def result(data: Tolietdata):
    return jsonable_encoder(opid.Query_Number_of_urination(data.username,data.starttime, data.stoptime, data.uid))


@app.post('/Number_of_urination02/')
async def result(request: Request):
    user_data = await request.json()
    # 处理用户数据
    # print('values:', user_data['values']['uid'])
    uid = user_data['values']['uid']
    # start_time = user_data['values']['timeRange'][0]
    # stop_time = user_data['values']['timeRange'][1]
    start_time = datetime.fromisoformat(user_data['values']['timeRange'][0].split(".")[0])
    stop_time = datetime.fromisoformat(user_data['values']['timeRange'][1].split(".")[0])
    print(type(start_time))
    print('values:', start_time, stop_time, uid)
    return jsonable_encoder(opid.Query_Number_of_urination(start_time, stop_time, uid))


@app.post('/login/account')
async def result(request:Request):
    json=await request.json()
    password,username,type=json['password'],json['username'],json['type']
    hash_password = hashlib.sha512(password.encode(encoding='UTF-8')).hexdigest()+'\n'
    #数据库查询
    client = pymongo.MongoClient("mongodb+srv://tomcat:cuityjs@cluster0.3ucwlxn.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.health
    col=db.users
    query = {"username": username}
    result = col.find_one(query)
    print(username)
    print(result['password'])
    print(hash_password)
    #判断
    if username == 'zhang' and result['password']==hash_password:
        body = {
            "status":"ok",
            "type":type,
            "currentAuthority":"Fzhang",
            }
        return body
    elif username =='wang' and result['password']==hash_password:
        body = {
            'status':'ok',
            'type':type,
            'currentAuthority':'Fwang',
        }
        return body
    else:
        body = {
            'status':'error',
            'type':type,
            'currentAuthority':'Fguest',
        }
        return body


if __name__ == '__main__':
    uvicorn.run('run:app', host="0.0.0.0", port=8000, reload=True)