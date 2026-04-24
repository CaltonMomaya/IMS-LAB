# Inventory Management System

A RESTful API and command-line interface for managing inventory, with integration to the OpenFoodFacts external product database.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [CLI Commands](#cli-commands)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

## Features

- Full CRUD operations for inventory items via REST API
- Command-line interface for all inventory actions
- Integration with OpenFoodFacts API to fetch product details by barcode or name
- In‑memory data storage (array‑based) for quick prototyping
- Robust error handling for invalid inputs and external API failures
- Unit tests covering API endpoints, CLI commands, and external API interactions

## Technology Stack

- Python 3.8+
- Flask (web framework)
- Flask‑RESTful (REST API extension)
- Requests (HTTP client for external API)
- Click (CLI framework)
- Pytest (testing framework)

## Installation

### 1. Clone or download the project

Navigate to your desired directory and ensure the following files exist:

- `app.py` – main Flask application
- `cli.py` – command-line interface
- `requirements.txt` – Python dependencies
- `tests/` – unit test directory

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # On Linux/macOS
venv\Scripts\activate           # On Windows
3. Install dependencies
bash
pip install -r requirements.txt
If you do not have a requirements.txt file, create one with:

bash
pip install flask requests click pytest pytest-cov
pip freeze > requirements.txt
Configuration
No additional configuration is required. The API runs on http://localhost:5000 by default.
You can change the port by editing the last line of app.py:

python
app.run(debug=True, host='0.0.0.0', port=5000)   # change port number as needed
If you change the port, also update the API_BASE_URL variable in cli.py.

Running the Application
The system consists of two parts: the Flask API server (must be kept running) and the CLI client.

Start the API server (Terminal 1)
bash
cd ~/IMS
source venv/bin/activate
python app.py
Expected output:

text
Inventory API running on http://localhost:5000
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
Keep this terminal open.

Use the CLI (Terminal 2)
Open a new terminal and run:

bash
cd ~/IMS
source venv/bin/activate
python cli.py --help
Now you can execute any of the CLI commands described below.

API Endpoints
All endpoints return JSON. The base URL is http://localhost:5000.

Method	Endpoint	Description	Request Body (JSON)	Response
GET	/inventory	List all items	–	{"status":"success","data":[...],"count":n}
GET	/inventory/<id>	Get single item	–	{"status":"success","data":{...}}
POST	/inventory	Add new item	{"name":"...","price":float,"quantity":int, "brand":"...","description":"...","barcode":"..."}	{"status":"success","message":"..."}
PATCH	/inventory/<id>	Update item	Any subset of fields from POST	{"status":"success","data":{...}}
DELETE	/inventory/<id>	Delete item	–	{"status":"success","message":"..."}
GET	/external/product?barcode=<code>	Fetch product by barcode from OpenFoodFacts	–	{"status":"success","data":{...}}
GET	/external/product?name=<name>	Search product by name (uses sample fallback if API fails)	–	Same as above
Example API Calls
bash
# List all items
curl http://localhost:5000/inventory

# Get item with id 1
curl http://localhost:5000/inventory/1

# Add a new item
curl -X POST http://localhost:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"name":"Orange Juice","price":3.99,"quantity":50,"brand":"Tropicana"}'

# Update price of item 5
curl -X PATCH http://localhost:5000/inventory/5 \
  -H "Content-Type: application/json" \
  -d '{"price":4.49}'

# Delete item 5
curl -X DELETE http://localhost:5000/inventory/5

# Search external product by barcode (real API)
curl "http://localhost:5000/external/product?barcode=737628064502"

# Search by name (uses sample data)
curl "http://localhost:5000/external/product?name=milk"
CLI Commands
All commands are invoked with python cli.py <command>.

Command	Description	Example
list	Show all inventory items	python cli.py list
view <id>	Show details of a single item	python cli.py view 1
add	Interactive addition of an item	python cli.py add
update <id>	Update an item (provide options)	python cli.py update 1 --price 5.99 --quantity 60
delete <id>	Delete an item (asks for confirmation)	python cli.py delete 5
find	Search external API and optionally add to inventory	python cli.py find --name milk or --barcode 737628064502
CLI Options for add
When you run python cli.py add, you will be prompted for:

Product name (required)

Price (required)

Quantity (required)

Brand (optional)

Description (optional)

Barcode (optional)

CLI Options for update
You can update one or more fields:

bash
python cli.py update 1 --name "New Name" --price 9.99 --quantity 30 --brand "New Brand" --description "Updated description"
CLI Example Session
bash
$ python cli.py list
Total items: 4

ID: 1
Name: Organic Almond Milk
Price: $4.99
Quantity: 50
Brand: Silk
Barcode: 123456789012

$ python cli.py find --name coffee
Product found:
Name: Coffee Beans
Brand: Starbucks
Category: Beverages
Description: Premium roasted coffee beans
Do you want to add this product to inventory? [y/N]: y
Enter price: 12.99
Enter quantity: 30
Product added to inventory successfully!

$ python cli.py update 1 --quantity 60
Success: Item updated

$ python cli.py delete 5
Are you sure you want to delete item 5? [y/N]: y
Success: Item deleted
Testing
Unit tests cover API endpoints, CLI commands, and external API interactions using pytest and mocking.

Run all tests
bash
pytest tests/ -v
Run with coverage report
bash
pytest tests/ --cov=. --cov-report=term
Run specific test file
bash
pytest tests/test_routes.py -v
pytest tests/test_external.py -v
Important: Stop the Flask server (Ctrl+C) before running the tests, because pytest starts its own test client.

Test output example
text
tests/test_external.py::test_search_by_barcode PASSED
tests/test_external.py::test_search_by_name_fallback PASSED
tests/test_external.py::test_missing_parameter PASSED
tests/test_routes.py::test_get_all_items PASSED
tests/test_routes.py::test_get_single_item PASSED
tests/test_routes.py::test_get_nonexistent_item PASSED
tests/test_routes.py::test_add_item PASSED
tests/test_routes.py::test_update_item PASSED
tests/test_routes.py::test_delete_item PASSED

============================== 9 passed in 0.32s ==============================
Troubleshooting
ModuleNotFoundError: No module named 'flask'
Activate the virtual environment and run pip install -r requirements.txt.

Connection refused when using CLI
Ensure the Flask server is running in a separate terminal (python app.py).

Check that the port in cli.py (API_BASE_URL) matches the port in app.py.

404 Not Found on API endpoints
Verify that you are using the correct URL.

Make sure the server is running and that you are using the app.py from this project (not a different one).

Port 5000 already in use
Change the port in app.py (e.g., to 5001) and update API_BASE_URL in cli.py accordingly.

External API returns error
The system falls back to sample data for common product names (milk, coffee, bread, chocolate, eggs). For barcode searches, it uses the real OpenFoodFacts API. If the external API is unavailable or rate‑limited, you will see a message indicating fallback data.

Project Structure
text
~/IMS/
├── app.py                 # Flask application with all API endpoints
├── cli.py                 # Command-line interface
├── requirements.txt       # Python dependencies
├── README.md              # This documentation
├── tests/
│   ├── __init__.py
│   ├── test_routes.py     # Unit tests for API endpoints
│   └── test_external.py   # Unit tests for external API integration
└── venv/                  # Virtual environment (ignored by Git)
License
This project is provided for educational purposes as part of a software development lab.

Author: Inventory Management System Lab
Last Updated: April 2026
