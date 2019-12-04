
# Yolov3 detection
Detect object in video with [darknet YoloV3 method](https://pjreddie.com/darknet/yolo/)

## Python environment
- Version: Python 3.6.8
- requirments:
```
numpy==1.17.4
opencv-python==4.1.2.30
pymongo==3.9.0
redis==3.3.11
```
- Test in: Ubuntu 18.04.3 LTS

## Setup for YoloV3
Put the following file in `darkent/` folder
- [yolov3.cfg](https://github.com/pjreddie/darknet/tree/master/cfg)
- [yolov3.weights](https://pjreddie.com/media/files/yolov3.weights)

test video `yolotest.mp4` is from https://www.youtube.com/watch?v=vF1RPI6j7b0

## Openfass handler
1. asynchandler.py
2. handler.py

### asynchandler.py
handle trigger process request

- url: e.g. `http://127.0.0.1:31112/function/process`
- request body: filename:String, e.g. `yolotest.mp4`
- response body: userid (object id in MongoDB process collection)

Check MongoDB process collection to get the process status.

test: see `asynchandlerTest.py`

### handler.py
handle detection

- url: e.g. `http://127.0.0.1:31112/function/detection`
- request body: filename:String, e.g. `yolotest.mp4`
- response body: (ignore)

Check MongoDB user collection with userid to get the processed images.

test: see `handlerTest.py`

## Database
Redis and MongoDB

### Redis
Store video binary

schema:
```Json
{
    "key":String, //videoname 
    "value": Bytes, //videoBytes
```

test: see `asynchandlerTest.py`

### MongoDB
Database has one collection for all users process and one collection per user name.
- Database name: `comp4651`
- Users process collection name: `process`
- User collection name pattern: `user_<videoname>`, e.g. `user_yolotest.mp4`

test: see `handlerTest.py`

#### User process
Store all users process.

status: 
- `pending`: processing
- `done`: processed
- `removed`: user's collection removed

schema:
```Javascript
{
    "_id":ObjectId, //userobject id
    "username": String, //videoname 
    "status": String, //process status
}
```

get particular user status:
```python
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
comp4651DB = mongoclient["comp4651"]
processCol = comp4651DB["process"]
status = processCol.find_one({"_id":userid})["status"]
```

#### User collection
schema:
```Javascript
{
    "_id":ObjectId, //image id
    "frameno": String, //frame number
    "name": String, //image name
    "userid": String, //user object id string
    "base64": Bytes, //base64 encoded jpg,
}
```

get all image of the user:
```python
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
comp4651DB = mongoclient["comp4651"]
comp4651DB["user_"+str(videoname)].find({"userid":userid}).sort("frameno")
```


base64 for test in client: `yolotest.mp4_0.jpg.txt`
- `data:image/jpeg;base64, <base64>`
