from urllib import response
import requests
from datetime import datetime
import json


params={"starttime":datetime(2021,1,1,0,0,0).isoformat(),
    "stoptime":datetime(2022,1,1,0,0,0).isoformat(),
    "uid":1}
data=json.dumps(params)
url = f'http://127.0.0.1:8000/Time_Period_Data/'
print(url)
ret = requests.post(url,json=data)

print(data)
print(ret)
print(ret.text)
# 如果返回的数据不是json格式，打印json格式会报错
# print(ret.json())