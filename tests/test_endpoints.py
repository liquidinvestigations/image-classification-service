import pytest
from app import get_app


@pytest.fixture
def client():
    app = get_app()
    app.config['TESTING'] = True
    return app.test_client()


def test_health_check(client):
    rv = client.get('/health')
    assert rv.status_code == 200
