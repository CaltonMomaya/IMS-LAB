import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_items(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'data' in data

def test_get_single_item(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['data']['id'] == 1

def test_get_nonexistent_item(client):
    response = client.get('/inventory/999')
    assert response.status_code == 404

def test_add_item(client):
    new_item = {
        'name': 'Test Product',
        'price': 9.99,
        'quantity': 10,
        'brand': 'TestBrand'
    }
    response = client.post('/inventory', json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['name'] == 'Test Product'

def test_update_item(client):
    updates = {'price': 7.99, 'quantity': 25}
    response = client.patch('/inventory/1', json=updates)
    assert response.status_code == 200
    data = response.get_json()
    assert data['data']['price'] == 7.99

def test_delete_item(client):
    new_item = {'name': 'Temp Delete', 'price': 1.99, 'quantity': 5}
    post_resp = client.post('/inventory', json=new_item)
    temp_id = post_resp.get_json()['data']['id']
    delete_resp = client.delete(f'/inventory/{temp_id}')
    assert delete_resp.status_code == 200
    get_resp = client.get(f'/inventory/{temp_id}')
    assert get_resp.status_code == 404
