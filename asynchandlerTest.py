from redisController import redisController
import globalconstant as gvar
from asynchandler import handle

#test
#save redis
temp = redisController(gvar.REDIS_HOST,gvar.REDIS_PORT)
videoname = "yolotest.mp4"
with open(videoname,"r+b") as src:
    videoBytes = src.read()
temp.saveVideo(videoname,videoBytes) 

#request
print(handle(videoname))
