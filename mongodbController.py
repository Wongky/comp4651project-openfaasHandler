#ref: https://www.runoob.com/python3/python-mongodb.html

import pymongo #pymongo-3.9.0 https://pypi.org/project/pymongo/
#from bson.objectid import ObjectId

#run mongo server `$./mongod`

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
comp4651DB = mongoclient["comp4651"]
processCol = comp4651DB["process"] #user process collection

#status: pending, done, removed
#=======================================================#

#return objectid
def insertUserProcess(username,status="pending"):
    return processCol.insert_one(
        {"username":username,"status":status}
    ).inserted_id

#status="done"
#return True if updated
def updateUserProcess(objectid):
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
def getUserProcess(objectid):
    result = processCol.find_one({"_id":objectid})
    return result["status"]
#print(getUserProcess(ObjectId("5de71d051d7cf1955bd01da5")))

#=======================================================#

#return collection name
def createuserdb(username,replace=False):
    colname = "user_"+str(username)
    if replace:
        if colname in comp4651DB.list_collection_names(): #replace same user
            print("username database exists. removing")
            #remove username status
            processCol.update_many(
                {"username":username},
                { "$set": { "status": "removed" }}
            )
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
