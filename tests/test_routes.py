import pytest
import json
from app import create_app
from app.models import inventory_db, InventoryItem

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Clear database before each test
        inventory_db.clear()
        # Add test data
        test_item = InventoryItem("Test Item", 10.99, 5)
        inventory_db.append(test_item)
        yield client

def test_get_all_items(client):
    """Test GET /inventory endpoint"""
    response = client.get('/inventory')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['name'] == 'Test Item'

def test_get_single_item(client):
    """Test GET /inventory/<id> endpoint"""
    item_id = inventory_db[0].id
    response = client.get(f'/inventory/{item_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['name'] == 'Test Item'

def test_get_nonexistent_item(client):
    """Test GET with invalid ID"""
    response = client.get('/inventory/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['status'] == 'error'

def test_add_item(client):
    """Test POST /inventory endpoint"""
    new_item = {
        'name': 'New Product',
        'price': 15.99,
        'quantity': 10
    }
    response = client.post('/inventory', 
                          data=json.dumps(new_item),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['data']['name'] == 'New Product'

def test_update_item(client):
    """Test PATCH /inventory/<id> endpoint"""
    item_id = inventory_db[0].id
    updates = {'price': 12.99, 'quantity': 8}
    response = client.patch(f'/inventory/{item_id}',
                            data=json.dumps(updates),
                            content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['data']['price'] == 12.99
    assert data['data']['quantity'] == 8

def test_delete_item(client):
    """Test DELETE /inventory/<id> endpoint"""
    item_id = inventory_db[0].id
    response = client.delete(f'/inventory/{item_id}')
    assert response.status_code == 200
    # Verify item is deleted
    response = client.get(f'/inventory/{item_id}')
    assert response.status_code == 404