import redistrigger as rt

def event_handler_test(msg):
    key, operation = rt.messageDecode(msg)
    if operation == "set":
        print("{} is {}".format(key ,operation))
        test(key)

rt.event_listener(event_handler_test)
