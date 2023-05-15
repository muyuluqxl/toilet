import numpy as np
import matplotlib.pyplot as plt
import math
from pprint import pprint
import radar
import datetime

uriaList=["ph","protein","glucose","ketone_body","blood","bilirubin","urocholegen","nitrite","leucocyte_esterase","vitamin_C"]

miumapping = {
    "ph":6.2,
    "protein":0.11,
    "glucose":2.9,
    "ketone_body":1.2,
    #"blood":false,
    "bilirubin":9.5,
    "urocholegen":1.5,
    "nitrite":60000,
    "leucocyte_esterase":9,
    "vitamin_C":60,
}

sigmamapping={
    "ph":0.05,
    "protein":0.0001,
    "glucose":1,
    "ketone_body":0.01,
    #"blood":false,
    "bilirubin":0.1,
    "urocholegen":0.04,
    "nitrite":10000000,
    "leucocyte_esterase":1.6,
    "vitamin_C":10,
}
"""     
    "ph":0.05,
    "protein":0.0001,
    "glucose":0.2,
    "ketone_body":0.01,
    #"blood":false,
    "bilirubin":0.1,
    "urocholegen":0.04,
    "nitrite":10000000,
    "leucocyte_esterase":1.6,
    "vitamin_C":10,


    "ph":0.2,
    "protein":0.0001,
    "glucose":1,
    "ketone_body":0.1,
    #"blood":false,
    "bilirubin":1,
    "urocholegen":0.04,
    "nitrite":100000000,
    "leucocyte_esterase":2,
    "vitamin_C":100, """

drawmapping = {
    "ph":(4,9),
    "protein":(-0.05,0.2),
    "glucose":(-0.5,2.8),
    "ketone_body":(-0.5,3.5),
    #"blood":false,
    "bilirubin":(6,15),
    "urocholegen":(0.13,3.55),
    "nitrite":(0,100000),
    "leucocyte_esterase":(0.5,15),
    "vitamin_C":(20,100),
}

class GuassianGenerator:
    def __init__(self,index,miu,sigma,day) -> None:
        self.index = index
        self.areain = drawmapping[index]
        self.miu = miu
        self.sigma = sigma
        self.day = day
        self.value = None
    
    def dataprint(self):
        if self.value is None:
            self.value=np.random.normal(loc=self.miu, scale=self.sigma, size=(self.day,1))
            mask=np.asarray(self.value>0,dtype=float)
        return self.value*mask
    
    def draw_guassian(self):
        X=np.linspace(self.areain[0],self.areain[1],100)
        Y = 1 / (np.sqrt(2 * math.pi) * np.sqrt(self.sigma))*np.exp(-(X - self.miu)**2 / (2 * self.sigma))
        mask=np.asarray(X>0,dtype=float)
        Y*=mask
        plt.figure(figsize=(7,3))
        plt.plot(X,Y)
        plt.show()

class BloodGenerator:
    def __init__(self,day,precent):
        self.day=day
        self.precent=precent
    def dataprint(self):
        value=np.random.rand(self.day,1)
        mask=np.asarray(value>self.precent,dtype=float)
        return value*mask

def numOfData(daysOfTheYear=365):
    timesOfDays=np.random.randint(1,3,size=(daysOfTheYear,1))
    day=timesOfDays.sum()
    return day,timesOfDays

def TrandomdataList(timeOfDays):
    tList=[]
    for index,num in enumerate(timeOfDays):
        daybase=datetime.datetime(2022,1,1,6,0,0,0)
        daymorning=daybase+datetime.timedelta(days=index)
        daynight=daymorning+datetime.timedelta(hours=18)
        for i in range(num[0]):
            timestamp = radar.random_datetime(daymorning,daynight)
            tList.append(timestamp)
    return tList
  
def MrandomdataList(familynum,times,uid):
    mList=[]
    metadata={}
    for time in range(times):
        metadata["from"]="toilet-"+familynum
        metadata["type"]="urine"
        metadata["uid"]=uid
        mList.append(metadata)
    return mList

def UrandomdataList(times):
    # Udic={}
    UList=[]
    genList={}
    for g in uriaList:
        if g=="blood":
            genList[g]=BloodGenerator(times,1).dataprint()
            continue
        gener=GuassianGenerator(g,miumapping[g],sigmamapping[g],times)
        genList[g]=gener.dataprint()
    for time in range(times):
        Udic={} # edit here
        for key in uriaList:
            Udic[key]=round(genList[key][time].item(),8)
        UList.append(Udic)
        #print(UList)
    return UList

