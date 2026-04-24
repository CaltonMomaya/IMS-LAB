from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory_db = [
    {"id": 1, "name": "Organic Almond Milk", "price": 4.99, "quantity": 50, "description": "Unsweetened organic almond milk", "brand": "Silk", "barcode": "123456789012"},
    {"id": 2, "name": "Whole Grain Bread", "price": 3.49, "quantity": 100, "description": "100% whole wheat bread", "brand": "Nature's Own", "barcode": "234567890123"},
    {"id": 3, "name": "Free Range Eggs", "price": 5.99, "quantity": 75, "description": "Grade A large eggs", "brand": "Eggland's Best", "barcode": "345678901234"},
    {"id": 4, "name": "Coffee Beans", "price": 12.99, "quantity": 30, "description": "Premium roasted coffee", "brand": "Starbucks", "barcode": "737628064502"}
]
next_id = 5

SAMPLE_PRODUCTS = {
    'milk': {'name': 'Organic Milk', 'brand': 'Organic Valley', 'description': 'Fresh organic whole milk', 'category': 'Dairy', 'barcode': '123456789012'},
    'coffee': {'name': 'Coffee Beans', 'brand': 'Starbucks', 'description': 'Premium roasted coffee beans', 'category': 'Beverages', 'barcode': '737628064502'}
}

@app.route('/')
def index():
    return jsonify({'name': 'Inventory API', 'version': '1.0', 'status': 'running'})

@app.route('/inventory', methods=['GET'])
def get_all():
    return jsonify({'status': 'success', 'data': inventory_db, 'count': len(inventory_db)})

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_one(item_id):
    item = next((i for i in inventory_db if i['id'] == item_id), None)
    if item:
        return jsonify({'status': 'success', 'data': item})
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

@app.route('/inventory', methods=['POST'])
def add_item():
    global next_id
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data or 'quantity' not in data:
        return jsonify({'status': 'error', 'message': 'Missing fields'}), 400
    new_item = {
        'id': next_id, 'name': data['name'], 'price': float(data['price']),
        'quantity': int(data['quantity']), 'description': data.get('description'),
        'brand': data.get('brand'), 'barcode': data.get('barcode')
    }
    inventory_db.append(new_item)
    next_id += 1
    return jsonify({'status': 'success', 'message': 'Added', 'data': new_item}), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((i for i in inventory_db if i['id'] == item_id), None)
    if not item:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404
    data = request.get_json()
    for key in ['name', 'price', 'quantity', 'description', 'brand', 'barcode']:
        if key in data:
            item[key] = data[key] if key != 'price' else float(data[key])
    return jsonify({'status': 'success', 'message': 'Updated', 'data': item})

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global inventory_db
    item = next((i for i in inventory_db if i['id'] == item_id), None)
    if not item:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404
    inventory_db = [i for i in inventory_db if i['id'] != item_id]
    return jsonify({'status': 'success', 'message': 'Deleted'})

@app.route('/external/product', methods=['GET'])
def external_product():
    barcode = request.args.get('barcode')
    name = request.args.get('name')
    if not barcode and not name:
        return jsonify({'status': 'error', 'message': 'Need barcode or name'}), 400
    if barcode:
        try:
            r = requests.get(f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json', timeout=5)
            data = r.json()
            if data.get('status') == 1:
                p = data['product']
                return jsonify({'status': 'success', 'data': {
                    'name': p.get('product_name', 'Unknown'),
                    'brand': p.get('brands', 'Unknown'),
                    'description': p.get('ingredients_text', ''),
                    'category': p.get('categories', ''),
                    'barcode': barcode
                }})
        except:
            pass
        return jsonify({'status': 'error', 'message': 'Product not found'}), 404
    else:
        name_lower = name.lower()
        if name_lower in SAMPLE_PRODUCTS:
            return jsonify({'status': 'success', 'data': SAMPLE_PRODUCTS[name_lower]})
        return jsonify({'status': 'error', 'message': 'Not found'}), 404

if __name__ == '__main__':
    print("Inventory API running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
