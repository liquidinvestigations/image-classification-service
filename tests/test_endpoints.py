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


def test_health_check(client):
    resp = client.get('/health')
    assert resp.status_code == 200


def test_object_detection(client):
    with open('tests/data/bicycles.jpg', 'rb') as f:
        data = {
            'image': (f, 'bicycle.jpg'),
        }
        resp = client.post('/detect-objects', content_type='multipart/form-data', data=data)
    assert resp.status_code == 200
