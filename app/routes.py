from flask_restful import Resource, reqparse
from flask import jsonify, request
from app.services.inventory_service import InventoryService
from app.services.openfoodfacts_service import OpenFoodFactsService

class InventoryListResource(Resource):
    """Resource for handling multiple inventory items"""
    
    def get(self):
        """GET /inventory - Fetch all items"""
        items = InventoryService.get_all_items()
        return jsonify({
            'status': 'success',
            'data': items,
            'count': len(items)
        })
    
    def post(self):
        """POST /inventory - Add a new item"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name is required')
        parser.add_argument('price', type=float, required=True)
        parser.add_argument('quantity', type=int, required=True)
        parser.add_argument('barcode')
        parser.add_argument('description')
        parser.add_argument('brand')
        parser.add_argument('category')
        
        args = parser.parse_args()
        
        try:
            new_item = InventoryService.add_item(args)
            return jsonify({
                'status': 'success',
                'message': 'Item added successfully',
                'data': new_item
            }), 201
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400

class InventoryItemResource(Resource):
    """Resource for handling single inventory item"""
    
    def get(self, item_id):
        """GET /inventory/<id> - Fetch single item"""
        item = InventoryService.get_item(item_id)
        if item:
            return jsonify({
                'status': 'success',
                'data': item
            })
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    
    def patch(self, item_id):
        """PATCH /inventory/<id> - Update an item"""
        update_data = request.get_json()
        updated_item = InventoryService.update_item(item_id, update_data)
        
        if updated_item:
            return jsonify({
                'status': 'success',
                'message': 'Item updated successfully',
                'data': updated_item
            })
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404
    
    def delete(self, item_id):
        """DELETE /inventory/<id> - Remove an item"""
        if InventoryService.delete_item(item_id):
            return jsonify({
                'status': 'success',
                'message': 'Item deleted successfully'
            })
        return jsonify({
            'status': 'error',
            'message': 'Item not found'
        }), 404

class ExternalProductResource(Resource):
    """Resource for fetching external product data"""
    
    def get(self):
        """GET /external/product - Fetch product from external API"""
        parser = reqparse.RequestParser()
        parser.add_argument('barcode')
        parser.add_argument('name')
        args = parser.parse_args()
        
        if args.barcode:
            product = OpenFoodFactsService.fetch_product_by_barcode(args.barcode)
        elif args.name:
            product = OpenFoodFactsService.search_product_by_name(args.name)
        else:
            return jsonify({
                'status': 'error',
                'message': 'Either barcode or name is required'
            }), 400
        
        if product:
            return jsonify({
                'status': 'success',
                'data': product
            })
        return jsonify({
            'status': 'error',
            'message': 'Product not found'
        }), 404

def initialize_routes(api):
    """Initialize all API routes"""
    api.add_resource(InventoryListResource, '/inventory')
    api.add_resource(InventoryItemResource, '/inventory/<string:item_id>')
    api.add_resource(ExternalProductResource, '/external/product')