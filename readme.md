
# Yolov3 detection openfaas handler
Detect object in video with [darknet YoloV3 method](https://pjreddie.com/darknet/yolo/)

Project:
- [web](https://github.com/ytlamal/comp4651_project)
- [object detection process](https://github.com/Wongky/comp4651project-openfaasHandler)
- [container](https://github.com/sheldonchiu/Comp4651-Project)

## Python environment
- Version: Python 3.6.8
- requirments:
```
numpy==1.17.4
opencv-python==4.1.2.30
pymongo==3.9.0
redis==3.3.11
```
- Locally Tested in: 
    - os: Ubuntu 18.04.3 LTS
    - redis: Redis 5.0.6 (00000000/0) 64 bit
    - mongodb: mongodb-linux-x86_64-ubuntu1804-4.2.1

- build openfaas Tested in:
    - minikube
    - Kubernetes
    - follow [this](https://medium.com/faun/getting-started-with-openfaas-on-minikube-634502c7acdf)

## Setup

### Setup for YoloV3
Put the following file in `<cwd>/darkent/` folder
- [coco.names](https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names)
- [yolov3.cfg](https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg)
- [yolov3.weights](https://pjreddie.com/media/files/yolov3.weights)

### global constant
change constant in `globalconstant.py`

## handler
**handler.py** (openfaas handler)
- handle detection

**redistrigger.py** (docker images)
- listen to redis and trigger detection

### test in local device: 

setup:
- run redis server in a terminal
```shell
$ redis-server
```
- run mongodb in another terminal
```shell
$ cd /usr/local/mongodb/bin
$ ./mongod --dbpath=<some path with directory created>
```

test muliple videos:
- set redis notification in terminal `$ redis-cli config set notify-keyspace-events KEA`
1. run `redistriggerTest.py` to listen to video submission and trigger yolo detection
2. run `clinetTest.py` to submit create username and submit video to redis
3. repeat step 2 to test muliple videos (can edit the videoname)

test sample output:
```shell
$ python3 redistrigger.py
{'type': 'psubscribe', 'pattern': None, 'channel': b'__keyspace@0__:*', 'data': 1}
Handler {'type': 'pmessage', 'pattern': b'__keyspace@0__:*', 'channel': b'__keyspace@0__:yolotest.mp4', 'data': b'set'}
yolotest.mp4 is set
video temp path:  /tmp/yolotest.mp4
Reading Frame...
username: yolotest.mp4, userid: 5dec4fda2d3399b3632d30fb is removed
Userid:  False
Handler {'type': 'pmessage', 'pattern': b'__keyspace@0__:*', 'channel': b'__keyspace@0__:yolotest.mp4', 'data': b'set'}
yolotest.mp4 is set
video temp path:  /tmp/yolotest.mp4
Reading Frame...
Read Frame total:  19
Userid:  5dec4fddd6ab3378ab4d098b
```

single video test:
1. run `clinetTest.py` to submit create username and submit video to redis
2. run `handlerTest.py` if video is in redis

test sample output:
```shell
$ python3 handlerTest.py 
video temp path:  /tmp/yolotest.mp4
Reading Frame...
Read Frame total:  19
Userid:  5de78728d1694216c0eb0ee7
```
test video `yolotest.mp4` is from https://www.youtube.com/watch?v=vF1RPI6j7b0

### Build

#### Build openfaas function

requirments for yolodetection:
```
numpy==1.17.4
opencv-python==4.1.2.30
pymongo==3.9.0
redis==3.3.11
```

##### create openfaas handler:
```shell
$ faas-cli template pull https://github.com/openfaas-incubator/python3-debian
$ faas-cli new --lang python3-debian yolodetection
```

put file in it:
```
yolodetection.yml (auto gen by fass-cli)
yolodetection/
├── handler.py   #replace with handler.py
├── mypackage
│   ├── globalconstant.py
│   ├── mongodbController.py
│   ├── redisController.py
│   ├── darknet.py
│   └── __init__.py 
├── __init__.py  #replace with "docker/yolodetection/__init__.py" (for additional module method2)
└── requirements.txt   #replace with "docker/yolodetection/requirements.txt"
```

replace `template/python3-debian/Dockerfile` with `openfaas/Dockerfile`

##### build:

```shell
$ faas-cli build -f yolodetection.yml
```

**More option:**
handle additional module import
- Method1: add path in `yolodetection/__init__.py`, e.g.
```python
import sys

#change the location
sys.path.append("/home/app/function")
```
- Method2: use --build-arg `ADDITIONAL_PACKAGE_FOLDERNAME=<path to package relate to yolodetection/>`: copy folder in `build/yolodetection/function` to python env of function container, e.g.
```shell
$ faas-cli build -f yolodetection.yml --build-arg ADDITIONAL_PACKAGE_FOLDERNAME=mypackage
```

handle additional file
- Method1 : modify the `template/python3-debian/Dockerfile` to store the file, e.g.
```
RUN mkdir -p darknet
WORKDIR ${VAR_CWD}/darknet
RUN wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
```
- Method2: use --build-arg `ADDITIONAL_FILE_FOLDERNAME=<path to package relate to yolodetection/>`: copy folder in `build/yolodetection/function` to cwd of function container, e.g.
```shell
$ faas-cli build -f yolodetection.yml --build-arg ADDITIONAL_FILE_FOLDERNAME=darknet
```

#### Build redistrigger docker image

requirments for redistrigger:
```
redis==3.3.11
requests2==2.16.0
```

folder structure
redistrigger/
├── redistrigger.py
├── mypackage
│   ├── globalconstant.py
│   ├── redisController.py
│   └── __init__.py 
└──__init__.py  #replace with "docker/redistrigger/__init__.py" (for additional module method2)

build in docker image ...

### How To Call openfaas Handler
- url: e.g. `http://127.0.0.1:31112/async-function/yolodetection`
- set header: e.g. `X-Callback-Url=http://127.0.0.1:31112/function/other`
- request body: filename:String, e.g. `yolotest.mp4`
- response body: userid at lastline; e.g.
```
remove:  user_yolotest.mp4
username: yolotest.mp4, userid: 5dea6815d956f9d4dca5dff5, collection name: user_yolotest.mp4
video temp path:  /tmp/yolotest.mp4
Reading Frame...
Read Frame total:  19
Userid:  5dea6815d956f9d4dca5dff5
5dea6815d956f9d4dca5dff5
```
After calling, check MongoDB user collection with userid to get the processed images. see "User process" below 


or user redistrigger listen to video uploaded and call yolodetection automatically 
- set redis notification `$ redis-cli config set notify-keyspace-events KEA`

## Database
Redis and MongoDB

### Redis
Store video binary

schema:
```Javascript
{
    "key":String, //videoname 
    "value": Bytes, //videoBytes
```

test: see `asynchandlerTest.py`

### MongoDB
Database has one collection for all users process and one collection per user name. If duplicated user name, remove collection of older user name. 
- Database name: `comp4651`
- Users process collection name: `process`
- User collection name pattern: `user_<videoname>`, e.g. `user_yolotest.mp4`

test: see `handlerTest.py`

#### User process
Store all users process.

status: 
- `submitted` : user submitted form
- `pending`: detection processing
- `done`: detection processed
- `removed`: user's collection removed

schema:
```Javascript
{
    "_id":ObjectId, //userobject id (generated by mongodb)
    "username": String, //videoname 
    "status": String, //process status
}
```

action done by client before upload video to redis:
- If duplicated user name, remove collection of older user name.
```python
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
comp4651DB = mongoclient["comp4651"]
processCol = comp4651DB["process"]

#remove username status=submitted,pending,done
processCol.update_many(
    {"username":username},
    { "$set": { "status": "removed" }}
)

colname = "user_"+str(username)
# remove collection of user name
if colname in comp4651DB.list_collection_names():
    comp4651DB[colname].drop()
#create new user of the user name
userid = str(processCol.insert_one(
            {"username":username,"status":"submitted"}
        ).inserted_id)
```

To get particular user status:
```python
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
comp4651DB = mongoclient["comp4651"]
processCol = comp4651DB["process"]
status = processCol.find_one({"_id":userid})["status"]
```

To get user objectid of same username:
```python
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
comp4651DB = mongoclient["comp4651"]
processCol = comp4651DB["process"]
result = processCol.find({"username":username, "status" : {$not: "removed"}})
for x in result:
    #status = submitted or pending or done
    userid = str(x["_id"])
    break
```

#### User collection
store all processed images of a username

schema:
```Javascript
{
    "_id":ObjectId, //image id (generated by mongodb)
    "frameno": float, //frame number
    "name": String, //image name (pattern `<username>_<frameno>.jpg`)
    "userid": String, //user object id string
    "base64": String, //base64 encoded jpg,
}
```

To get all image of the user:
```python
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
comp4651DB = mongoclient["comp4651"]
comp4651DB["user_"+str(videoname)].find({"userid":userid}).sort("frameno")
```

base64 for test in client: `yolotest.mp4_0.jpg_w.txt`
- `data:image/jpeg;base64, <base64>`
