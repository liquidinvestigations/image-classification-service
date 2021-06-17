# image-classification-service
REST service with image classification and object detection

# Usage
At the moment the service supports object detection which can be enabled by setting the `OBJECT_DETECTION_ENABLED` environment variable to `true`.

## Routes

Use `POST /detect-objects` to receive JSON-data containing the detected objects, the probability and the position of the detected object in the image. An example call with curl would look like this:
`curl -F 'image=@test.jpg'  http://baseurl/detect-objects`.

To check if the service is up you can use `/health`, which will return HTTP 200, if everything is running.

## Choosing a model
There are three supported models which are `RetinaNet`, `YOLOv3` and `TinyYOLOv3`. To choose which model will be used to detect objects set the `OBJECT_DETECTION_MODEL` environment variable to either `yolo`, `tiny_yolo` or `retina`.

## Setting up waitress
The service uses `waitress`as a server and exposes port `5001`. The amount of threads used by waitress can be controlled through the environment variable `WAITRESS_THREADS` which is set in the Dockerfile.

## Running tests locally
To run the tests locally using `drone`, execute `./run_tests.sh`.

# Stats while running the Models on 'testdata'

## RetinaNet (Model Size: 145 MB)
Runtime: 5:34 min  
Ressources needed:  50.000 Mhz CPU (Peak), 7.000 MB Memory (taken from Nomads container overview)  
5M Duration: 20.192628  
5M Fill: 1023.04%  
5M: 152  

## YOLOv3 (Model Size: 237 MB)
Runtime: 10:21 min  
Ressources needed: 4800 Mhz CPU (20.000 Peak), 3.000 MB Memory (taken from Nomads container overview)  
5M Duration: 1569.58%  
5M Fill: 54.752632  
5M: 86  

## TinyYOLOv3 (Model Size: 34 MB)
Runtime: 10:35 min  
Ressources needed: 5.000 Mhz CPU (8.000 Peak), 3.300 MB Memory (taken from Nomads container overview)  
5M Duration: 55.691765  
5M Fill: 1468.03%  
5M: 82  




