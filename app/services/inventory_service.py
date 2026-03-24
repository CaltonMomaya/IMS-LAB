from app.models import InventoryItem, inventory_db
from typing import List, Dict, Optional

class InventoryService:
    """Service layer for inventory operations"""
    
    @staticmethod
    def get_all_items() -> List[Dict]:
        """Get all inventory items"""
        return [item.to_dict() for item in inventory_db]
    
    @staticmethod
    def get_item(item_id: str) -> Optional[Dict]:
        """Get a single inventory item by ID"""
        for item in inventory_db:
            if item.id == item_id:
                return item.to_dict()
        return None
    
    @staticmethod
    def add_item(item_data: Dict) -> Dict:
        """Add a new inventory item"""
        new_item = InventoryItem(
            name=item_data['name'],
            price=item_data.get('price', 0),
            quantity=item_data.get('quantity', 0),
            barcode=item_data.get('barcode'),
            description=item_data.get('description'),
            brand=item_data.get('brand'),
            category=item_data.get('category')
        )
        inventory_db.append(new_item)
        return new_item.to_dict()
    
    @staticmethod
    def update_item(item_id: str, update_data: Dict) -> Optional[Dict]:
        """Update an existing inventory item"""
        for item in inventory_db:
            if item.id == item_id:
                item.update(update_data)
                return item.to_dict()
        return None
    
    @staticmethod
    def delete_item(item_id: str) -> bool:
        """Delete an inventory item"""
        for i, item in enumerate(inventory_db):
            if item.id == item_id:
                inventory_db.pop(i)
                return True
        return False