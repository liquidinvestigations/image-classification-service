"""Flask app that provides endpoints to detect objects in an image and classify images."""

from imageai.Detection import ObjectDetection
from imageai.Classification import ImageClassification
import os
import io
import numpy as np
import cv2
from flask import Flask, request, jsonify, Response, abort
import logging
from waitress import serve
from PIL import Image
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.applications.densenet import preprocess_input

app = Flask(__name__)

logger = logging.getLogger('waitress')

execution_path = os.getcwd()


def get_boolean(env):
    return os.getenv(env, 'False').lower() in ('true', 't')


# get the boolean value of the str environment variables
OBJECT_DETECTION_ENABLED = get_boolean('OBJECT_DETECTION_ENABLED')
IMAGE_CLASSIFICATION_ENABLED = get_boolean('IMAGE_CLASSIFICATION_ENABLED')
VECTOR_GENERATION_ENABLED = get_boolean('VECTOR_GENERATION_ENABLED')


def image_to_np(image_file):
    """Convert image file to numpy array."""

    return cv2.imdecode(np.frombuffer(image_file.read(), dtype=np.uint8), -1)


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
        detector.setModelPath(
            os.path.join(execution_path, "models/detect/yolo.h5"))
    if model == "tiny_yolo":
        detector.setModelTypeAsTinyYOLOv3()
        detector.setModelPath(
            os.path.join(execution_path, "models/detect/yolo-tiny.h5"))
    if model == "retina":
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath(
            os.path.join(execution_path,
                         "models/detect/resnet50_coco_best_v2.1.0.h5"))
    detector.loadModel()
    return detector


def setup_prediction():
    """Setup for image prediction with a model.


    This function sets the image classifier to use the model specified by the
    environment variable IMAGE_CLASSIFICATION_MODEL. The four available options are
    'mobilenet', 'resnet', 'inception' and 'densenet'. As a side effect this functions
    also imports the correct 'preprocess_input' which is required to get the feature vector from the
    classification model.

    Returns:
        An ImageClassification object.
    """
    prediction = ImageClassification()
    model = os.getenv('IMAGE_CLASSIFICATION_MODEL')
    if model == "mobilenet":
        prediction.setModelTypeAsMobileNetV2()
        prediction.setModelPath(
            os.path.join(execution_path, "models/classify/mobilenet_v2.h5"))
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    if model == "resnet":
        prediction.setModelTypeAsResNet()
        prediction.setModelPath(
            os.path.join(execution_path,
                         "models/classify/resnet50_imagenet_tf.2.0.h5"))
        from tensorflow.keras.applications.resnet50 import preprocess_input # noqa F811
    if model == "inception":
        prediction.setModelTypeAsInceptionV3()
        prediction.setModelPath(
            os.path.join(
                execution_path,
                "models/classify/inception_v3_weights_tf_dim_ordering_tf_kernels.h5"
            ))
        from tensorflow.keras.applications.inception_v3 import preprocess_input # noqa F811
    if model == "densenet":
        prediction.setModelTypeAsDenseNet121()
        prediction.setModelPath(
            os.path.join(execution_path,
                         "models/classify/DenseNet-BC-121-32.h5"))
        from tensorflow.keras.applications.densenet import preprocess_input # noqa F401, F811
    prediction.loadModel()
    return prediction


if OBJECT_DETECTION_ENABLED:
    detector = setup_detector()

if IMAGE_CLASSIFICATION_ENABLED or VECTOR_GENERATION_ENABLED:
    prediction = setup_prediction()
    if VECTOR_GENERATION_ENABLED:
        base_model = prediction._ImageClassification__model_collection[0]
        layer = next(x for x in base_model.layers if isinstance(x, GlobalAveragePooling2D))
        vector_model = Model(inputs=base_model.input, outputs=layer.output)


@app.route('/detect-objects', methods=['POST'])
def detect_objects():
    """Object detectoin endpoint.

    This endpoint receives an image and runs object detection on that image.

    Returns:
        A JSON Response with the detected objects and scores of the image.
        If the image cannot be processed returns HTTP 500 and if the service is not enabled
        returns HTTP 403.
    """
    if not OBJECT_DETECTION_ENABLED:
        abort(403, description="Object detection is not enabled.")

    image_file = request.files['image']
    try:
        image_np = image_to_np(image_file)
        _, detections = detector \
            .detectObjectsFromImage(input_type='array',
                                    input_image=image_np,
                                    minimum_percentage_probability=30,
                                    output_type='array')
    except ValueError as e:
        logger.warning(e)
        return Response("Error processing the image.", status=500)
    return jsonify(detections)


@app.route('/classify-image', methods=['POST'])
def classify_image():
    """Image classification endpoint.

    This endpoint receives an image and runs image classification on that image.

    Returns:
        A JSON Response containing the classifications and the corresponding scores (HTTP 200).
        If the image cannot be processed returns HTTP 500 and if the service is not enabled
        returns HTTP 403.
    """
    if not IMAGE_CLASSIFICATION_ENABLED:
        abort(403, description="Image classification is not enabled.")

    image_file = request.files['image']

    try:
        image_np = image_to_np(image_file)
        predictions, probabilities = prediction.classifyImage(
            input_type='array', image_input=image_np, result_count=10)
        zipped_results = list(zip(predictions, probabilities))
    except ValueError as e:
        logger.warning(e)
        return Response("Error processing the image.", status=500)
    return jsonify(zipped_results)


def process_image(image_file):
    """Preprocess an image so that it can be fed into the model.

    Processes a given FileStorage object and returns the image as a preprocessed
    numpy array.
    """
    target_size = (224, 224)
    img = Image.open(io.BytesIO(image_file.read()))
    img = img.convert('RGB')
    img = img.resize(target_size)
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img


@app.route('/get-vector', methods=['POST'])
def get_vector():
    """Image feature-vector generation endpoint.

    This endpoint receives an image and extracts a feature-vector from it.

    Returns:
        A JSON Response containing the feature-vector as a list and the model used to
        create that vector (HTTP 200). The length of the
        vector depends on the model used and will be either 1024, 1280 or 2048.
        If the image cannot be processed returns HTTP 500 and if the service is not enabled
        returns HTTP 403.
    """
    if not VECTOR_GENERATION_ENABLED:
        abort(403, description="Vector generation is not enabled.")
    image_file = request.files['image']
    img = process_image(image_file)
    vector = vector_model.predict(img).flatten()
    return jsonify(model=os.getenv('IMAGE_CLASSIFICATION_MODEL'), vector=vector.tolist())


@app.route('/health')
def health_check():
    """Health Check endpoint.

    This endopoint checks if the service is up and running.

    Returns:
        HTTP 200 if the service is reachable.
    """
    return Response(status=200)


@app.route('/status')
def status():
    """Endpoint to get the current status of the service.

    This endpoints returns information about the activated functionality and the models used.

    Returns:
        A JSON Response containing information about the functionalities (classification
        and detection) and their current status.
    """
    res = {
        'image-classification': {
            'enabled': IMAGE_CLASSIFICATION_ENABLED,
            'model': os.getenv('IMAGE_CLASSIFICATION_MODEL')
        },
        'object-detection': {
            'enabled': OBJECT_DETECTION_ENABLED,
            'model': os.getenv('OBJECT_DETECTION_MODEL')
        },
        'image-vector': {
            'enabled': VECTOR_GENERATION_ENABLED,
            'model': os.getenv('IMAGE_CLASSIFICATION_MODEL')
        },
    }
    return jsonify(res)


def get_app():
    """Returns the app for testing.

    Returns:
        the app, for testing.
    """
    return app


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5001)
