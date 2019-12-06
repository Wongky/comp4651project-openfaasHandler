#test YoloV3 class

from mypackage.darknet import Yolov3
from mypackage import globalconstant as gvar

imagefile = "darknet/data/dog.jpg"
outfile = "object-detection.jpg"

yolo = yolov3.Yolov3(gvar.classesfile,gvar.configfile,gvar.weightfile)

yolo.detectImagefile(imagefile,outfile)
