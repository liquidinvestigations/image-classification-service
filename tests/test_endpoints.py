import pytest
import sys
import json
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import app


@pytest.fixture
def client():
    flask_app = app.get_app()
    flask_app.config['TESTING'] = True
    return flask_app.test_client()


def test_health_check(client):
    resp = client.get('/health')
    assert resp.status_code == 200


def test_object_detection(client):
    with open('tests/data/bike.jpg', 'rb') as f:
        data = {
            'image': (f, 'bike.jpg'),
        }
        resp = client.post('/detect-objects',
                           content_type='multipart/form-data',
                           data=data)
    assert resp.status_code == 200


def test_image_classification(client):
    with open('tests/data/bike.jpg', 'rb') as f:
        data = {
            'image': (f, 'bike.jpg'),
        }
        resp = client.post('/classify-image',
                           content_type='multipart/form-data',
                           data=data)
    assert resp.status_code == 200


def test_status(client):
    resp = client.get('/status')
    status = {
        'image-classification': {
            'enabled': True,
            'model': 'mobilenet'
        },
        'object-detection': {
            'enabled': True,
            'model': 'yolo'
        }
    }
    assert json.loads(resp.data) == status


def test_vector_generation(client):
    with open('tests/data/bike.jpg', 'rb') as f:
        data = {
            'image': (f, 'bike.jpg'),
        }
        resp = client.post('/get-vector',
                           content_type='multipart/form-data',
                           data=data)
    assert resp.status_code == 200


def test_classify_unavailable(client):
    app.IMAGE_CLASSIFICATION_ENABLED = False
    with open('tests/data/bike.jpg', 'rb') as f:
        data = {
            'image': (f, 'bike.jpg'),
        }
        resp_classify = client.post('/classify-image',
                                    content_type='multipart/form-data',
                                    data=data)
    assert resp_classify.status_code == 403


def test_detection_unavailable(client):
    app.OBJECT_DETECTION_ENABLED = False
    with open('tests/data/bike.jpg', 'rb') as f:
        data = {
            'image': (f, 'bike.jpg'),
        }
        resp_detect = client.post('/detect-objects',
                                  content_type='multipart/form-data',
                                  data=data)
    assert resp_detect.status_code == 403


def test_vector_generation_unavailable(client):
    app.VECTOR_GENERATION_ENABLED = False
    with open('tests/data/bike.jpg', 'rb') as f:
        data = {
            'image': (f, 'bike.jpg'),
        }
        resp = client.post('/get-vector',
                           content_type='multipart/form-data',
                           data=data)
    assert resp.status_code == 403
