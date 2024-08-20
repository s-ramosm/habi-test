import pytest
from flask import json
from app import app

# Mock para el controlador y excepciones
from unittest.mock import patch, MagicMock
from src.controlers.immovables import ImmovableControler
from src.core.exceptions import FilterNotAllowed

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_immovables_success(client):
    with patch('app.ImmovableControler') as MockImmovableControler:
        mock_controller = MockImmovableControler.return_value
        mock_controller.get_all.return_value = {"immovables": ["property1", "property2"]}

        response = client.get('/')
        assert response.status_code == 200
        assert json.loads(response.data) == {"immovables": ["property1", "property2"]}

def test_get_all_immovables_filter_not_allowed(client):
    with patch('app.ImmovableControler') as MockImmovableControler:
        mock_controller = MockImmovableControler.return_value
        mock_controller.get_all.side_effect = FilterNotAllowed()

        response = client.get('/')
        assert response.status_code == 400
        assert json.loads(response.data) == {"msg": "One or more filters in your request are not allowed"}

def test_get_all_immovables_value_error(client):
    with patch('app.ImmovableControler') as MockImmovableControler:
        mock_controller = MockImmovableControler.return_value
        mock_controller.get_all.side_effect = ValueError()

        response = client.get('/')
        assert response.status_code == 400
        assert json.loads(response.data) == {"msg": "Year format incorrect"}

def test_get_all_immovables_server_error(client):
    with patch('app.ImmovableControler') as MockImmovableControler:
        mock_controller = MockImmovableControler.return_value
        mock_controller.get_all.side_effect = Exception()

        response = client.get('/')
        assert response.status_code == 500
        assert json.loads(response.data) == {"msg": "Server error"}
