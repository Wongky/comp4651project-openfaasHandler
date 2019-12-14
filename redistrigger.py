#listen to redis and trigger detection

#https://redis.io/topics/pubsub
#https://www.cnblogs.com/leguan1314/p/9642859.html

# $ redis-cli config set notify-keyspace-events KEA
import redis #redis 3.3.11: https://pypi.org/project/redis/
import time
from mypackage import globalconstant as gvar
import requests

def messageDecode(msg):
    print('Handler', msg)
    key = msg["channel"].decode("utf-8").split("__keyspace@0__:",1)[1]
    operation = msg["data"].decode("utf-8")
    return key, operation

def event_handler(msg):
    payload, operation = messageDecode(msg)
    if operation == "set":
        print("{} is {}".format(payload ,operation))
        
        #https://stackoverflow.com/questions/57458203/how-should-i-pass-text-plain-data-to-pythons-requests-post
        header = {"Content-type": 'text/plain',"charset":"utf-8", "Accept": "text/plain"}

        r = requests.post(
            gvar.YOLO_DETECTION_URL, 
            data=payload.encode('utf-8'), 
            headers=header
        )
        if r.status_code == requests.codes.ok:
            print("OK")
        elif r.status_code == requests.codes.accepted:
            print("Accepted and Processing")
        else:
            print(r.status_code)
        print(r.text)

def event_listener(eventhandler):
    connection = redis.StrictRedis(host=gvar.REDIS_HOST, port=gvar.REDIS_PORT)
    pubsub = connection.pubsub()
    pubsub.psubscribe(**{'__keyspace@0__:*': eventhandler})

    while True:
        message = pubsub.get_message()
        if message:
            print(message)
        else:
            time.sleep(0.01)

def handle(req="ignore"):
    event_listener(event_handler)
