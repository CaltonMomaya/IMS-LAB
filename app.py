"""
Inventory Management System - Simple Flask Application
"""
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# In-memory database
inventory_db = [
    {"id": 1, "name": "Organic Almond Milk", "price": 4.99, "quantity": 50, 
     "description": "Unsweetened organic almond milk", "brand": "Silk", "barcode": "123456789012"},
    {"id": 2, "name": "Whole Grain Bread", "price": 3.49, "quantity": 100, 
     "description": "100% whole wheat bread", "brand": "Nature's Own", "barcode": "234567890123"},
    {"id": 3, "name": "Free Range Eggs", "price": 5.99, "quantity": 75, 
     "description": "Grade A large eggs", "brand": "Eggland's Best", "barcode": "345678901234"},
    {"id": 4, "name": "Coffee Beans", "price": 12.99, "quantity": 30, 
     "description": "Premium roasted coffee", "brand": "Starbucks", "barcode": "737628064502"}
]
next_id = 5

# Sample product database for when API is unavailable
SAMPLE_PRODUCTS = {
    'milk': {
        'name': 'Organic Milk',
        'brand': 'Organic Valley',
        'description': 'Fresh organic whole milk, pasteurized and homogenized',
        'category': 'Dairy',
        'barcode': '123456789012'
    },
    'coffee': {
        'name': 'Coffee Beans',
        'brand': 'Starbucks',
        'description': 'Premium roasted coffee beans',
        'category': 'Beverages',
        'barcode': '737628064502'
    },
    'bread': {
        'name': 'Whole Grain Bread',
        'brand': "Nature's Own",
        'description': '100% whole wheat bread with no artificial preservatives',
        'category': 'Bakery',
        'barcode': '234567890123'
    },
    'chocolate': {
        'name': 'Dark Chocolate Bar',
        'brand': 'Lindt',
        'description': '70% cocoa dark chocolate, smooth and rich',
        'category': 'Confectionery',
        'barcode': '123456789012'
    },
    'eggs': {
        'name': 'Free Range Eggs',
        'brand': 'Eggland\'s Best',
        'description': 'Grade A large eggs, rich in omega-3',
        'category': 'Dairy',
        'barcode': '345678901234'
    }
}

@app.route('/')
def index():
    """Home page with API information"""
    return jsonify({
        'name': 'Inventory Management System API',
        'version': '1.0',
        'status': 'running',
        'total_items': len(inventory_db),
        'endpoints': {
            'GET /inventory': 'List all inventory items',
            'GET /inventory/<id>': 'Get a specific item',
            'POST /inventory': 'Add a new item',
            'PATCH /inventory/<id>': 'Update an item',
            'DELETE /inventory/<id>': 'Delete an item',
            'GET /external/product?barcode=<code>': 'Fetch product from OpenFoodFacts',
            'GET /external/product?name=<name>': 'Search product in OpenFoodFacts'
        }
    })

@app.route('/inventory', methods=['GET'])
def get_all_items():
    """Get all inventory items"""
    return jsonify({
        'status': 'success',
        'data': inventory_db,
        'count': len(inventory_db)
    })

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a single inventory item"""
    item = next((item for item in inventory_db if item['id'] == item_id), None)
    if item:
        return jsonify({'status': 'success', 'data': item})
    return jsonify({'status': 'error', 'message': 'Item not found'}), 404

@app.route('/inventory', methods=['POST'])
def add_item():
    """Add a new inventory item"""
    global next_id
    
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'name' not in data:
        return jsonify({'status': 'error', 'message': 'Name is required'}), 400
    if 'price' not in data:
        return jsonify({'status': 'error', 'message': 'Price is required'}), 400
    if 'quantity' not in data:
        return jsonify({'status': 'error', 'message': 'Quantity is required'}), 400
    
    new_item = {
        'id': next_id,
        'name': data['name'],
        'price': float(data['price']),
        'quantity': int(data['quantity']),
        'description': data.get('description'),
        'brand': data.get('brand'),
        'barcode': data.get('barcode')
    }
    
    inventory_db.append(new_item)
    next_id += 1
    
    return jsonify({
        'status': 'success',
        'message': 'Item added successfully',
        'data': new_item
    }), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    """Update an inventory item"""
    item = next((item for item in inventory_db if item['id'] == item_id), None)
    if not item:
        return jsonify({'status': 'error', 'message': 'Item not found'}), 404
    
    if not request.is_json:
        return jsonify({'status': 'error', 'message': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        item['name'] = data['name']
    if 'price' in data:
        item['price'] = float(data['price'])
    if 'quantity' in data:
        item['quantity'] = int(data['quantity'])
    if 'description' in data:
        item['description'] = data['description']
    if 'brand' in data:
        item['brand'] = data['brand']
    if 'barcode' in data:
        item['barcode'] = data['barcode']
    
    return jsonify({
        'status': 'success',
        'message': 'Item updated successfully',
        'data': item
    })

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an inventory item"""
    global inventory_db
    item = next((item for item in inventory_db if item['id'] == item_id), None)
    if not item:
        return jsonify({'status': 'error', 'message': 'Item not found'}), 404
    
    inventory_db = [item for item in inventory_db if item['id'] != item_id]
    
    return jsonify({
        'status': 'success',
        'message': 'Item deleted successfully'
    })

@app.route('/external/product', methods=['GET'])
def external_product():
    """Fetch product from OpenFoodFacts API"""
    barcode = request.args.get('barcode')
    name = request.args.get('name')
    
    if not barcode and not name:
        return jsonify({
            'status': 'error',
            'message': 'Either barcode or name parameter is required'
        }), 400
    
    try:
        if barcode:
            # Fetch by barcode
            url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
            headers = {'User-Agent': 'InventoryManagementSystem/1.0'}
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 1 and data.get('product'):
                product_data = data['product']
                result = {
                    'name': product_data.get('product_name', 'Unknown'),
                    'brand': product_data.get('brands', 'Unknown'),
                    'description': product_data.get('ingredients_text', 'No description available')[:300],
                    'category': product_data.get('categories', 'Uncategorized'),
                    'barcode': barcode
                }
                return jsonify({'status': 'success', 'data': result})
            else:
                return jsonify({'status': 'error', 'message': 'Product not found'}), 404
                
        elif name:
            # Search by name
            search_url = "https://world.openfoodfacts.org/cgi/search.pl"
            params = {
                'search_terms': name,
                'search_simple': 1,
                'action': 'process',
                'json': 1,
                'page_size': 1,
                'fields': 'product_name,brands,ingredients_text,categories,code'
            }
            headers = {'User-Agent': 'InventoryManagementSystem/1.0'}
            
            try:
                response = requests.get(search_url, params=params, headers=headers, timeout=5)
                response.raise_for_status()
                data = response.json()
                
                if data.get('products') and len(data['products']) > 0:
                    product = data['products'][0]
                    result = {
                        'name': product.get('product_name', 'Unknown'),
                        'brand': product.get('brands', 'Unknown'),
                        'description': product.get('ingredients_text', 'No description available')[:300],
                        'category': product.get('categories', 'Uncategorized'),
                        'barcode': product.get('code', '')
                    }
                    return jsonify({'status': 'success', 'data': result})
                else:
                    # If no product found in API, check sample database
                    name_lower = name.lower()
                    if name_lower in SAMPLE_PRODUCTS:
                        return jsonify({
                            'status': 'success', 
                            'data': SAMPLE_PRODUCTS[name_lower],
                            'message': 'Sample data (product not found in OpenFoodFacts)'
                        })
                    else:
                        return jsonify({'status': 'error', 'message': f'Product "{name}" not found'}), 404
                        
            except requests.exceptions.RequestException:
                # If API fails, return sample data if available
                name_lower = name.lower()
                if name_lower in SAMPLE_PRODUCTS:
                    return jsonify({
                        'status': 'success',
                        'data': SAMPLE_PRODUCTS[name_lower],
                        'message': 'Sample data (OpenFoodFacts API temporarily unavailable)'
                    })
                else:
                    return jsonify({
                        'status': 'error',
                        'message': f'Unable to search for "{name}". OpenFoodFacts API unavailable. Try searching by barcode instead.'
                    }), 503
                
    except requests.exceptions.Timeout:
        return jsonify({'status': 'error', 'message': 'Request timeout - please try again'}), 504
    except requests.exceptions.ConnectionError:
        return jsonify({'status': 'error', 'message': 'Connection error - please check your internet'}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': f'API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    print("\nInventory Management System API")
    print("--------------------------------")
    print(f"Items in inventory: {len(inventory_db)}")
    print("\nAvailable endpoints:")
    print("  GET    /inventory                    - List all items")
    print("  GET    /inventory/<id>               - Get single item")
    print("  POST   /inventory                    - Add new item")
    print("  PATCH  /inventory/<id>               - Update item")
    print("  DELETE /inventory/<id>               - Delete item")
    print("  GET    /external/product?barcode=123 - Fetch from OpenFoodFacts")
    print("  GET    /external/product?name=milk   - Search OpenFoodFacts")
    print("\nServer running at: http://localhost:5000")
    print("Press CTRL+C to quit\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
