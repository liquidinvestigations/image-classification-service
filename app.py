from imageai.Detection import ObjectDetection
import os
import numpy as np
import cv2
from flask import Flask, request, jsonify, Response, abort
import sys

app = Flask(__name__)

execution_path = os.getcwd()


def setup_detector():
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
    return Response(status=200)


@app.route('/set-model', methods=['POST'])
def set_model():
    print('Hello there', file=sys.stderr)
    if request.form['model']:
        print(request.form['model'], file=sys.stderr)
        os.environ['OBJECT_DETECTION_MODEL'] = request.form['model']
        detector = setup_detector()
        print(detector._ObjectDetection__modelType, file=sys.stderr)
        return Response(status=200)
    else:
        abort(400)


def get_app():
    return app


if __name__ == "__main__":
    app.run()
