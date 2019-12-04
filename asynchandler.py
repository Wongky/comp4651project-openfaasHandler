#hander trigger process request

from mongodbController import mongodbController
import globalconstant as gvar

#req = "name.mp4"
#return user object id
def handle(username):
    """handle a request to the function
    Args:
        req (str): request body
    """
    db = mongodbController(gvar.MONGO_HOST,gvar.MONGO_PORT)
    colname = db.createuserdb(username,True)
    userid = db.insertUserProcess(username)
    #print("username: {}, userid: {}, collection name: {}".format(username,userid,colname))
    return userid
