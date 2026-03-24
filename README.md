#  Inventory Management System

A complete REST API and CLI tool for managing inventory with OpenFoodFacts API integration.

##  Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection (for external API)

### Installation

1. **Navigate to the project directory:**
```bash
cd ~/IMS-LAB


# Create virtual environment
python -m venv venv

# Activate it:
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install flask requests click

#to run open1st terminal and run
cd ~/IMS-LAB
source venv/bin/activate
python app.py

#output should look like 

INVENTORY MANAGEMENT SYSTEM API

 Items in inventory: 4

 Available endpoints:
   GET    /inventory                    - List all items
   GET    /inventory/<id>               - Get single item
   POST   /inventory                    - Add new item
   PATCH  /inventory/<id>               - Update item
   DELETE /inventory/<id>               - Delete item
   GET    /external/product?barcode=123 - Fetch from OpenFoodFacts
   GET    /external/product?name=milk   - Search OpenFoodFacts


Server running at: http://localhost:5000
 Press CTRL+C to quit

 #open termina2 and run

 cd ~/IMS-LAB
source venv/bin/activate
python cli.py --help

#cli usage examples

# List all inventory items
python cli.py list

# Add a new product
python cli.py add

# Search for products from external API
python cli.py find --name "milk"
python cli.py find --barcode "737628064502"

# Update an item
python cli.py update 1 --price 5.99 --quantity 60

# View a specific item
python cli.py view 1

# Delete an item
python cli.py delete 1

#cli usage examples
# List all inventory items
python cli.py list

# Add a new product
python cli.py add

# Search for products from external API
python cli.py find --name "milk"
python cli.py find --barcode "737628064502"

# Update an item
python cli.py update 1 --price 5.99 --quantity 60

# View a specific item
python cli.py view 1

# Delete an item
python cli.py delete 1

Testing
Test the API with curl:
bash
# Check if server is running
curl http://localhost:5000/

# List inventory
curl http://localhost:5000/inventory

# Add test item
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Product","price":9.99,"quantity":10}'

# Search external API
curl "http://localhost:5000/external/product?name=coffee"

Test CLI commands:
bash
python cli.py list
python cli.py add
python cli.py find --name "milk"
python cli.py update 1 --price 5.99
python cli.py view 1
python cli.py delete 1