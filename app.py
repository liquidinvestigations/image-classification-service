"""Flask app that provides endpoints to detect objects in an image."""

from imageai.Detection import ObjectDetection
import os
import numpy as np
import cv2
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

execution_path = os.getcwd()


def setup_detector():
    """Setup the detector with a model.

    This function sets the object detector to use the model specified by the
    environment variable OBJECT_DETECTION_MODEL. The three available options are
    'yolo', 'tiny_yolo' and 'retina'.

    Returns:
        An ObjectDetection object.
    """
    detector = ObjectDetection()
    model = os.getenv('OBJECT_DETECTION_MODEL')
    if model == "yolo":
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(os.path.join(execution_path, "yolo.h5"))
    if model == "tiny_yolo":
        detector.setModelTypeAsTinyYOLOv3()
        detector.setModelPath(os.path.join(execution_path, "yolo-tiny.h5"))
    if model == "retina":
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(os.path.join(execution_path,
                                           "resnet50_coco_best_v2.1.0.h5"))
    detector.loadModel()
    return detector


if os.getenv('OBJECT_DETECTION_ENABLED'):
    detector = setup_detector()


@app.route('/detect-objects', methods=['POST'])
def detect_objects():
    """Object detectoin endpoint.

    This endpoint receives an image and runs object detection on that image.

    Returns:
        A JSON Response with the detected objects and scores of the image.
    """
    image_file = request.files['image']
    image_np = cv2.imdecode(np.frombuffer(image_file.read(), dtype=np.uint8),
                            -1)
    _, detections = detector \
        .detectObjectsFromImage(input_type='array',
                                input_image=image_np,
                                minimum_percentage_probability=30,
                                output_type='array')
    return jsonify(detections)


@app.route('/health')
def health_check():
    """Health Check endpoint.

    This endopoint checks if the service is up and running.

    Returns:
        HTTP 200 if the service is reachable.
    """
    return Response(status=200)


def get_app():
    """Returns the app for testing.

    Returns:
        the app, for testing.
    """
    return app


if __name__ == "__main__":
    app.run()
