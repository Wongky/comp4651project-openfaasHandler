#test redis trigger
# $ redis-cli config set notify-keyspace-events KEA

import redistrigger as rt
from handlerTest import test

def event_handler_test(msg):
    key, operation = rt.messageDecode(msg)
    if operation == "set":
        print("{} is {}".format(key ,operation))
        test(key)

rt.event_listener(event_handler_test)
