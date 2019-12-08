#change constant in here

import os

classesfile = "darknet/coco.names"
configfile = "darknet/yolov3.cfg"
weightfile = "darknet/yolov3.weights"

REDIS_HOST = os.getenv("redis","127.0.0.1")
REDIS_PORT = "6379"

MONGO_HOST = os.getenv("mongo","localhost")
MONGO_PORT = "27017"

# uses a default of "gateway" when "gateway_hostname" is not set
OPENFASS_GATEWAY= os.getenv("gateway_hostname", "192.168.99.105") 
OPENFASS_PORT = "31112"
YOLO_DETECTION_URL="http://{}:{}/async-function/{}".format(OPENFASS_GATEWAY,OPENFASS_PORT,"yolodetection")
