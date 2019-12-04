import redisController as temp
from asynchandler import handle

#test
#save redis
videoname = "yolotest.mp4"
with open(videoname,"r+b") as src:
    videoBytes = src.read()
temp.saveVideo(videoname,videoBytes) 

#request
print(handle(videoname))
