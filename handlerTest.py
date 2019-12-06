#test
import base64
from mypackage.mongodbController import mongodbController
from mypackage import globalconstant as gvar
from handler import handle

db = mongodbController(gvar.MONGO_HOST,gvar.MONGO_PORT)
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
        # with open("{}{}_w.txt".format(outpath,x["name"]),"w") as des:
        #     des.write(x["base64"])
        out=base64.b64decode(x["base64"])
        with open("{}{}".format(outpath,x["name"]),"w+b") as des:
            des.write(out)
