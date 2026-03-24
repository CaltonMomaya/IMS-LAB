from datetime import datetime
import uuid

class InventoryItem:
    """Model representing an inventory item"""
    
    def __init__(self, name, price, quantity, barcode=None, 
                 description=None, brand=None, category=None):
        self.id = str(uuid.uuid4())[:8]  # Generate short unique ID
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
        self.barcode = barcode
        self.description = description
        self.brand = brand
        self.category = category
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert item to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'barcode': self.barcode,
            'description': self.description,
            'brand': self.brand,
            'category': self.category,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def update(self, data):
        """Update item attributes"""
        for key, value in data.items():
            if hasattr(self, key) and value is not None:
                if key in ['price', 'quantity']:
                    setattr(self, key, float(value) if key == 'price' else int(value))
                else:
                    setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()

# Mock database (array storage)
inventory_db = []

# Initialize with sample data
def initialize_sample_data():
    """Initialize the database with sample items"""
    if not inventory_db:
        sample_items = [
            InventoryItem("Organic Almond Milk", 4.99, 50, "123456789012", 
                         "Unsweetened organic almond milk", "Silk", "Beverages"),
            InventoryItem("Whole Grain Bread", 3.49, 100, "234567890123",
                         "100% whole wheat bread", "Nature's Own", "Bakery"),
            InventoryItem("Free Range Eggs", 5.99, 75, "345678901234",
                         "Grade A large eggs", "Eggland's Best", "Dairy")
        ]
        inventory_db.extend(sample_items)

# Call initialization
initialize_sample_data()