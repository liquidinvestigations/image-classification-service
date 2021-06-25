# image-classification-service
REST service with image classification and object detection

# Usage
The service supports object detection and image classification. Object detection can be enabled by setting the `OBJECT_DETECTION_ENABLED` environment variable to `true`. To enable image classification set the `IMAGE_CLASSIFICATION` environment variable.

## Routes
Use `POST /detect-objects` to receive JSON-data containing the detected objects, the probability and the position of the detected object in the image. An example call with curl would look like this:
`curl -F 'image=@test.jpg'  http://baseurl/detect-objects`.

Use `POST /classify-image` to receive JSON-data containing the predicted classes and the probability image. An example call with curl would look like this:
`curl -F 'image=@test.jpg'  http://baseurl/classify-image`.

Both endpoints will return `HTTP 500` if the image could be processed. If an endpoint is not enabled by settings the corresponding environment variable when running the container it will return `HTTP 403`.

To check if the service is up you can use `/health`, which will return HTTP 200, if everything is running.

## Choosing a model
### Object Detection
There are three supported models which are `RetinaNet`, `YOLOv3` and `TinyYOLOv3`. To choose which model will be used to detect objects set the `OBJECT_DETECTION_MODEL` environment variable to either `yolo`, `tiny_yolo` or `retina`.

### Image Classification
There are three supported models which are `MobileNetV2`, `ResNet50`, `InceptionV3` and `DenseNet121`. To choose which model will be used to detect objects set the `IMAGE_CLASSIFICATION_MODEL` environment variable to either `mobilenet`, `resnet`, `inception` or `densenet`.

## Setting up waitress
The service uses `waitress`as a server and exposes port `5001`. The amount of threads used by waitress can be controlled through the environment variable `WAITRESS_THREADS` which is set in the Dockerfile.

## Running tests locally
To run the tests locally using `drone`, execute `./run_tests.sh`.

# Stats while running the Models on 'testdata'

# Object Detection

## RetinaNet (Model Size: 145 MB)
Runtime: ~ 5:34 min  
Ressources needed:  50.000 Mhz CPU (Peak), 7.000 MB Memory (taken from Nomads container overview)  
5M Duration: 20.192628  
5M Fill: 1023.04%  
5M: 152  

## YOLOv3 (Model Size: 237 MB)
Runtime: ~ 10:21 min  
Ressources needed: 4.800 Mhz CPU (20.000 Peak), 3.000 MB Memory (taken from Nomads container overview)  
5M Duration: 54.752632  
5M Fill: 1569.58%
5M: 86  

## TinyYOLOv3 (Model Size: 34 MB)
Runtime: ~ 10:35 min  
Ressources needed: 5.000 Mhz CPU (8.000 Peak), 3.300 MB Memory (taken from Nomads container overview)  
5M Duration: 55.691765  
5M Fill: 1468.03%  
5M: 82  

# Image Classification

## MobileNetV2 (Model Size: 4.82 MB)
Runtime: ~ 1:53 min  
Ressources needed:  5800 Mhz CPU (One Single Peak), ? MB Memory (No significant usage shown in Nomads container overview)  
5M Duration: 0.777142  
5M Fill: 41.97%  
5M: 162  

## ResNet50 (Model Size: 98 MB)
Runtime: ~ 2:15 min  
Ressources needed:  3622 Mhz CPU (Peak), ? MB Memory (No significant memory usage visible)  
5M Duration: 0.671041  
5M Fill: 36.24%  
5M: 162  

## InceptionV3 (Model Size: 91.6 MB)
Runtime: ~ 1:44 min  
Ressources needed:  8463 Mhz CPU (Peak), ? MB Memory (No significant memory usage visible)  
5M Duration: 0.709005  
5M Fill: 38.29%  
5M: 162  

## DenseNet121 (Model Size: 31.6 MB)
Runtime: ~ 2:06 min  
Ressources needed:  25.000 Mhz CPU (Peak), ? MB Memory (No significant memory usage visible)  
5M Duration: 0.714724  
5M Fill: 38.60%  
5M: 162  


# Classification + Object Detection
## Most resource expensive model each (RetinaNet + DenseNet)
Combined Runtime: ~ 4:51 min  
CPU: 52.000 Mhz (Peak) around 20.000 - 30.000 Mhz most of the time  
RAM: ? (Probably Nomads monitor is not working correctly)  

## Least resource expensive model each (YoloV3 + ResNet50)
Combined Runtime: ~ 10:13 min  
CPU: 23.000 Mhz (Peak) around 4.800 Mhz most of the time  
RAM: ?  
