# image-classification-service
REST service with image classification, object detection and extraction of a feature-vector from an image.

# Usage
The service supports object detection and image classification. Object detection can be enabled by setting the `OBJECT_DETECTION_ENABLED` environment variable to `true`. To enable image classification set the `IMAGE_CLASSIFICATION_ENABLED` environment variable to `true`. To enable the feature-vector extraction set `VECTOR_GENERATION_ENABLED` to `true`.

## Routes
### /detect-objects
Use `POST /detect-objects` to receive JSON-data containing the detected objects, the probability and the position of the detected object in the image. An example call with curl would look like this:
`curl -F 'image=@test.jpg'  http://baseurl/detect-objects`.

### /classify-image
Use `POST /classify-image` to receive JSON-data containing the predicted classes and the probability image. An example call with curl would look like this:
`curl -F 'image=@test.jpg'  http://baseurl/classify-image`.

Both endpoints will return `HTTP 500` if the image could be processed. If an endpoint is not enabled by settings the corresponding environment variable when running the container it will return `HTTP 403`.

### /get-vector
It is also possible to use the service to extract a feature-vector from an image. This vector can be used for reverse image search. The endpoint for that functionality is `POST /get-vector`. It can be used in the same way, the other two endpoints work. The response will be a JSON containing the vector and the model which was used to compute the vector. The model will always be the same as defined by `IMAGE_CLASSIFICATION_MODEL`.

### /health
To check if the service is up you can use `/health`, which will return HTTP 200, if everything is running.

### /status
To receive information about the current status of the service and the enabled functionalities use `/status`. This will return a JSON looking like this:
```
{
  "image-classification":
    {"model":"densenet","enabled":true},
  "object-detection":
    {"model":"yolo","enabled":false}
  "image-vector": 
    {"enabled":true}
}
```

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

# Vector Extraction
## MobileNetV2 (Model Size: 4.82 MB)
Runtime: ~ 2 min  
Ressources needed: 8.600 Mhz CPU (Peak), ? MB Memory (No significant memory usage visible)  
5M Duration: 0.822562  
5M Fill: 44.42%  
5M: 162  

## ResNet50 (Model Size: 98 MB)
Runtime: ~ 2:06 min  
Ressources needed: 13.600 Mhz CPU (Peak), ? MB Memory (No significant memory usage visible)  
5M Duration: 1.218618  
5M Fill: 65.81%  
5M: 162  

## InceptionV3 (Model Size: 91.6 MB)
Runtime: ~ 1:51 min  
Ressources needed: 4.400 Mhz CPU (Peak), ? MB Memory (No significant memory usage visible)  
5M Duration: 1.027624  
5M Fill: 55.49%  
5M: 162  

## DenseNet121 (Model Size: 31.6 MB)
Runtime: ~ 2:07 min  
Ressources needed: 17.000 Mhz CPU (Peak), ? MB Memory (No significant memory usage visible)  
5M Duration: 1.242954  
5M Fill: 67.12%  
5M: 162  
