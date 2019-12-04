#manage redis

#https://redis.io/topics/quickstart
#https://redis.io/topics/data-types-intro

import redis #redis 3.3.11: https://pypi.org/project/redis/
import tempfile #another option (failed): #https://stackoverflow.com/questions/56972903/how-to-read-mkv-bytes-as-video/

#run redis server `$redis-server`

r = redis.Redis(
    host='127.0.0.1',
    port=6379, 
    password='')

#https://redis.io/topics/data-types 
#https://stackoverflow.com/questions/5606106/what-is-the-maximum-value-size-you-can-store-in-redis
#bytes value: max 512MB string len
def saveVideo(videoname,videoBytes):
    '''
    with open("in.mp4","r+b") as src:
        videoBytes = src.read()
    r.set('in.mp4', videoBytes)
    '''   
    r.set(videoname, videoBytes)

#temp file #https://stackoverflow.com/questions/36795267/writing-mp4-file-from-binary-string-python
#return videopath+filename
def getVideoTemppath(videoname):
    temppath = tempfile.gettempdir()
    videoTemppath = "{}/{}".format(temppath,videoname)
    print("video temp path: ",videoTemppath)
    value = r.get(videoname)
    with open(videoTemppath,"w+b") as des:
        des.write(value)
    return videoTemppath
