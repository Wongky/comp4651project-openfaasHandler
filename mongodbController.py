#manage mongo

#https://www.runoob.com/python3/python-mongodb.html

import pymongo #pymongo-3.9.0 https://pypi.org/project/pymongo/
from bson.objectid import ObjectId

#run mongo server `$./mongod`

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
comp4651DB = mongoclient["comp4651"] #DB name
processCol = comp4651DB["process"] #user process collection

def getObjectId(idstring):
    return ObjectId(idstring)

#status: pending, done, removed
#===================users process============================#

#return objectid string
def insertUserProcess(username,status="pending"):
    return str(processCol.insert_one(
        {"username":username,"status":status}
    ).inserted_id)

#status="done"
#return True if updated
def updateUserProcess(userid):
    objectid = getObjectId(userid)
    if getUserProcess(objectid)=="removed":
        print("Userid{} data is removed".format(objectid))
        return False
    else:
        processCol.update_one(
            {"_id":objectid},
            {"$set": {"status":"done"}}
        )
        return True

#return status
def getUserProcess(userid):
    objectid = getObjectId(userid)
    result = processCol.find_one({"_id":objectid})
    return result["status"]
#print(getUserProcess(ObjectId("5de71d051d7cf1955bd01da5")))

#return user objectId or False for not found
def getUserID(username):
    result = processCol.find({"username":username})
    for x in result:
        if x["status"]!="removed":
            return x["_id"]
    return False

#===================user image=============================#

#return collection name
def createuserdb(username,replace=False):
    colname = "user_"+str(username)
    if replace:
        #remove username status
        processCol.update_many(
            {"username":username},
            { "$set": { "status": "removed" }}
        )
        if colname in comp4651DB.list_collection_names(): #replace same user
            print("username database exists. removing")
            comp4651DB[colname].drop()
    return colname

#userid: user object id
#return objectid
def insertoneBase64(username,userid,frameno,imagename,base64):
    return comp4651DB["user_"+str(username)].insert_one(
        {"frameno":frameno,"name":imagename,"userid":userid,"base64":base64}
    ).inserted_id

#return base64
def getBase64(username,userid,frameno,imagename):
    result = comp4651DB["user_"+str(username)].find_one(
        {"frameno":frameno,"name":imagename,"userid":userid}
    )
    return result["base64"]

#find by objectid
#return base64
def getBase64ById(username,objectid):
    result = comp4651DB["user_"+str(username)].find_one(
        {"_id":objectid}
    )
    return result["base64"]

#return all dict sort by frame number
def getAllImage(username,userid):
    '''
    for x in result:
        print(x["frameno"],x["name"])
    '''
    return comp4651DB["user_"+str(username)].find({"userid":userid}).sort("frameno")
