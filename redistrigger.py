#redis trigger process

#https://redis.io/topics/pubsub
#https://www.cnblogs.com/leguan1314/p/9642859.html

# $ redis-cli config set notify-keyspace-events KEA
import redis #redis 3.3.11: https://pypi.org/project/redis/
import time
from mypackage import globalconstant as gvar
from handlerTest import test

connection = redis.StrictRedis(host=gvar.REDIS_HOST, port=gvar.REDIS_PORT)
pubsub = connection.pubsub()

def event_handler(msg):
    print('Handler', msg)
    key = msg["channel"].decode("utf-8").split("__keyspace@0__:",1)[1]
    operation = msg["data"].decode("utf-8")
    if operation == "set":
        print("{} is {}".format(key ,operation))
        test(key)

pubsub.psubscribe(**{'__keyspace@0__:*': event_handler})

while True:
    message = pubsub.get_message()
    if message:
        print(message)
    else:
        time.sleep(0.01)
