import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('requests.get')
def test_search_by_barcode(mock_get, client):
    mock_response = {
        'status': 1,
        'product': {
            'product_name': 'Mock Product',
            'brands': 'MockBrand',
            'ingredients_text': 'Mock ingredients',
            'categories': 'Mock Category'
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    
    response = client.get('/external/product?barcode=123456789')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['name'] == 'Mock Product'

def test_search_by_name_fallback(client):
    response = client.get('/external/product?name=milk')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'Organic Milk' in data['data']['name']

def test_missing_parameter(client):
    response = client.get('/external/product')
    assert response.status_code == 400
    data = response.get_json()
    assert 'Need barcode or name' in data['message']
