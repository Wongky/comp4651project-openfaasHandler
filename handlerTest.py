#test
import base64
import mongodbController as db
from handler import handle

username = "yolotest.mp4"
handle(username)
userid = db.getUserID(username)
print("Userid: ",userid)

#retrive image from mongo
outpath = "/home/y/Documents/comp4651/upload/uploadtext/out/"
if db.getUserProcess(userid) == "done":
    allimg = db.getAllImage(username,userid)
    for x in allimg:
        #print("image{} id: {}".format(x["frameno"],x["_id"]))
        out=base64.b64decode(x["base64"])
        with open("{}{}".format(outpath,x["name"]),"w+b") as des:
            des.write(out)
