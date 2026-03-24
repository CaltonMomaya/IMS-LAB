import pytest
from unittest.mock import Mock, patch
from app.services.openfoodfacts_service import OpenFoodFactsService
from app.services.inventory_service import InventoryService
from app.models import inventory_db, InventoryItem

def test_fetch_product_by_barcode_success():
    """Test successful product fetch by barcode"""
    mock_response = {
        'status': 1,
        'product': {
            'product_name': 'Test Product',
            'brands': 'Test Brand',
            'ingredients_text': 'Test ingredients',
            'categories': 'Test Category'
        }
    }
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        result = OpenFoodFactsService.fetch_product_by_barcode('123456789012')
        
        assert result is not None
        assert result['name'] == 'Test Product'
        assert result['brand'] == 'Test Brand'

def test_fetch_product_by_barcode_not_found():
    """Test product fetch with not found status"""
    mock_response = {'status': 0}
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        result = OpenFoodFactsService.fetch_product_by_barcode('123456789012')
        
        assert result is None

def test_inventory_service_add_item():
    """Test adding item through service"""
    inventory_db.clear()
    
    new_item = {
        'name': 'Service Test Item',
        'price': 20.99,
        'quantity': 15
    }
    
    result = InventoryService.add_item(new_item)
    
    assert result['name'] == 'Service Test Item'
    assert result['price'] == 20.99
    assert len(inventory_db) == 1

def test_inventory_service_update_item():
    """Test updating item through service"""
    inventory_db.clear()
    item = InventoryItem("Update Test", 5.99, 10)
    inventory_db.append(item)
    
    updates = {'price': 7.99, 'quantity': 20}
    result = InventoryService.update_item(item.id, updates)
    
    assert result is not None
    assert result['price'] == 7.99
    assert result['quantity'] == 20