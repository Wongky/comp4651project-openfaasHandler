#https://stackoverflow.com/questions/36795267/writing-mp4-file-from-binary-string-python
#https://stackoverflow.com/questions/56972903/how-to-read-mkv-bytes-as-video/

import cv2 #opencv-python 4.1.1.26 : https://pypi.org/project/opencv-python/
#import io
import base64
from darknet import Yolov3  #another option: https://pypi.org/project/darknetpy/
import mongodbController as db
import redisController as temp

videoname = "yolotest.mp4"
#save to redis
'''
with open(videoname,"r+b") as src:
    videoBytes = src.read()
temp.saveVideo(videoname,videoBytes)
'''

classesfile = "darknet/yolov3.txt"
configfile = "darknet/yolov3.cfg"
weightfile = "darknet/yolov3.weights"
yolo = Yolov3(classesfile,configfile,weightfile)

username = "Wongky"
colname = db.createuserdb(username,True)
userid = db.insertUserProcess(username)
print("username: {}, userid: {}, collection name: {}".format(username,userid,colname))

#https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
#print(cv2.__version__)
#vidcap = cv2.VideoCapture("yolotest.mp4") #video from: https://www.youtube.com/watch?v=vF1RPI6j7b0
vidcap = cv2.VideoCapture(temp.getVideoTemppath(videoname))
fps = vidcap.get(cv2.CAP_PROP_FPS)
#print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
success,image = vidcap.read()
totalframe = 0
frameno = 0
success = True
print("Reading Frame...")
while success:
    #cv2.imwrite("out/frame%d.jpg" % totalframe, image)     # save frame as JPEG file
    success,image = vidcap.read()
    #print ('Read frame{}:{}'.format(frameno,success))
    if success:
        outimage = yolo.detectFrame(image)
        #cv2.imwrite("out/out{}.jpg".format(totalframe), outimage) # save detection as JPEG file
        #https://stackoverflow.com/questions/40928205/python-opencv-image-to-byte-string-for-json-transfer/40930153
        retval, buffer = cv2.imencode('.jpg', outimage) # encode detection as JPEG
        #encode base64
        imageid = db.insertoneBase64(
        username,
        userid,
        frameno,
        "{}_{}.jpg".format(username,totalframe),
        base64.b64encode(buffer)
        )
        #print('image{} id: {}'.format(totalframe,imageid))

        #get frame per second
        #https://stackoverflow.com/questions/22704936/reading-every-nth-frame-from-videocapture-in-opencv
        frameno += fps
        vidcap.set(1, frameno)
        totalframe+=1
    else:
        vidcap.release()
        print("Read Frame total: ",str(totalframe))
        db.updateUserProcess(userid) #,"done"

#retrive image from mongo
'''
outpath = "/home/y/Documents/comp4651/comp4651project/uploadtext/out/"
if db.getUserProcess(userid) == "done":
    allimg = db.getAllImage(username,userid)
    for x in allimg:
        #print("image{} id: {}".format(x["frameno"],x["_id"]))
        out=base64.b64decode(x["base64"])
        with open("{}{}".format(outpath,x["name"]),"w+b") as des:
            des.write(out)
'''
