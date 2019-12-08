#test client save video to redis

from mypackage.redisController import redisController
from mypackage import globalconstant as gvar
from client import handle

videoname = "yolotest.mp4"

import os
inpath = os.getcwd()+"/"

#request
print(handle(videoname))

#test
#save redis
temp = redisController(gvar.REDIS_HOST,gvar.REDIS_PORT)
with open("{}{}".format(inpath,videoname),"r+b") as src:
    videoBytes = src.read()
temp.saveVideo(videoname,videoBytes) 
print("save %s to redis"%(videoname))
