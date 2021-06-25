import pytest
import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from app import get_app


@pytest.fixture
def client():
    app = get_app()
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture
def disable_services(monkeypatch):
    monkeypatch.setenv('OBJECT_CLASSIFICATION_ENABLED', False)
    monkeypatch.setenv('IMAGE_CLASSIFICATION_ENABLED', False)


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


def test_services_unavailable(client, disable_services):
    with open('tests/data/bike.jpg', 'rb') as f:
        data = {
            'image': (f, 'bike.jpg'),
        }
        resp_classify = client.post('/classify-image',
                                    content_type='multipart/form-data',
                                    data=data)
        resp_detect = client.post('/detect_objects',
                                  content_type='multipart/form-data',
                                  data=data)
    assert resp_classify.status_code == 403
    assert resp_detect.status_code == 403
