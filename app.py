from imageai.Detection import ObjectDetection
import os
import io
import numpy as np
import cv2
from flask import Flask, request, jsonify

app = Flask(__name__)

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path , "yolo.h5"))
detector.loadModel()

@app.route('/detect-objects', methods=['POST'])
def detect_objects():
    image_file = request.files['image']
    image_np = cv2.imdecode(np.frombuffer(image_file.read(), dtype=np.uint8), -1)
    _ ,detections = detector.detectObjectsFromImage(input_type='array', input_image=image_np, minimum_percentage_probability=30, output_type='array')
    return jsonify(detections)