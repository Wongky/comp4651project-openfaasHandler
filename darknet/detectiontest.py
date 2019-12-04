import yolov3

classesfile = "yolov3.txt"
configfile = "yolov3.cfg"
weightfile = "yolov3.weights"
imagefile = "data/dog.jpg"
outfile = "object-detection.jpg"

yolo = yolov3.Yolov3(classesfile,configfile,weightfile)

yolo.detectImagefile(imagefile,outfile)
