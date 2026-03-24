#!/usr/bin/env python3
"""
Command Line Interface for Inventory Management System
"""

import click
import requests
import json
from typing import Optional

API_BASE_URL = "http://localhost:5000"

class InventoryCLI:
    """CLI interface for inventory management"""
    
    @staticmethod
    def make_request(method: str, endpoint: str, data: Optional[dict] = None):
        """Make HTTP request to API"""
        url = f"{API_BASE_URL}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url)
            else:
                return None
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            click.echo("Error: Cannot connect to API server. Make sure it's running.")
            return None
        except requests.exceptions.RequestException as e:
            click.echo(f"Error: {e}")
            if hasattr(e, 'response') and e.response:
                click.echo(f"Response: {e.response.text}")
            return None
    
    @staticmethod
    def format_item(item):
        """Format a single item for display"""
        click.echo(f"\n{'='*50}")
        click.echo(f"ID: {item['id']}")
        click.echo(f"Name: {item['name']}")
        click.echo(f"Price: ${item['price']:.2f}")
        click.echo(f"Quantity: {item['quantity']}")
        if item.get('brand'):
            click.echo(f"Brand: {item['brand']}")
        if item.get('category'):
            click.echo(f"Category: {item['category']}")
        if item.get('description'):
            click.echo(f"Description: {item['description']}")
        click.echo(f"{'='*50}")

@click.group()
def cli():
    """Inventory Management System CLI"""
    pass

@cli.command()
def list():
    """List all inventory items"""
    result = InventoryCLI.make_request('GET', '/inventory')
    if result and result.get('status') == 'success':
        items = result.get('data', [])
        if items:
            click.echo(f"\nTotal items: {len(items)}")
            for item in items:
                InventoryCLI.format_item(item)
        else:
            click.echo("No items in inventory")

@cli.command()
@click.argument('item_id')
def view(item_id):
    """View a single inventory item"""
    result = InventoryCLI.make_request('GET', f'/inventory/{item_id}')
    if result and result.get('status') == 'success':
        InventoryCLI.format_item(result['data'])
    elif result:
        click.echo(f"Error: {result.get('message', 'Item not found')}")

@cli.command()
@click.option('--name', prompt='Product name', help='Name of the product')
@click.option('--price', prompt='Price', type=float, help='Product price')
@click.option('--quantity', prompt='Quantity', type=int, help='Stock quantity')
@click.option('--brand', help='Product brand')
@click.option('--category', help='Product category')
@click.option('--barcode', help='Product barcode')
@click.option('--description', help='Product description')
def add(name, price, quantity, brand, category, barcode, description):
    """Add a new inventory item"""
    data = {
        'name': name,
        'price': price,
        'quantity': quantity
    }
    if brand:
        data['brand'] = brand
    if category:
        data['category'] = category
    if barcode:
        data['barcode'] = barcode
    if description:
        data['description'] = description
    
    result = InventoryCLI.make_request('POST', '/inventory', data)
    if result and result.get('status') == 'success':
        click.echo(f"Success: {result['message']}")
        InventoryCLI.format_item(result['data'])

@cli.command()
@click.argument('item_id')
@click.option('--name', help='Product name')
@click.option('--price', type=float, help='Product price')
@click.option('--quantity', type=int, help='Stock quantity')
@click.option('--brand', help='Product brand')
@click.option('--category', help='Product category')
def update(item_id, name, price, quantity, brand, category):
    """Update an inventory item"""
    data = {}
    if name:
        data['name'] = name
    if price is not None:
        data['price'] = price
    if quantity is not None:
        data['quantity'] = quantity
    if brand:
        data['brand'] = brand
    if category:
        data['category'] = category
    
    if not data:
        click.echo("No fields to update")
        return
    
    result = InventoryCLI.make_request('PATCH', f'/inventory/{item_id}', data)
    if result and result.get('status') == 'success':
        click.echo(f"Success: {result['message']}")
        InventoryCLI.format_item(result['data'])
    elif result:
        click.echo(f"Error: {result.get('message', 'Update failed')}")

@cli.command()
@click.argument('item_id')
def delete(item_id):
    """Delete an inventory item"""
    click.confirm(f"Are you sure you want to delete item {item_id}?", abort=True)
    result = InventoryCLI.make_request('DELETE', f'/inventory/{item_id}')
    if result and result.get('status') == 'success':
        click.echo(f"Success: {result['message']}")
    elif result:
        click.echo(f"Error: {result.get('message', 'Delete failed')}")

@cli.command()
@click.option('--barcode', help='Product barcode')
@click.option('--name', help='Product name')
def find(barcode, name):
    """Find product from external API"""
    if not barcode and not name:
        click.echo("Please provide either --barcode or --name")
        return
    
    params = []
    if barcode:
        params.append(f"barcode={barcode}")
    if name:
        params.append(f"name={name}")
    
    result = InventoryCLI.make_request('GET', f'/external/product?{"&".join(params)}')
    if result and result.get('status') == 'success':
        product = result['data']
        click.echo(f"\n{'='*50}")
        click.echo(f"Product found:")
        click.echo(f"Name: {product.get('name', 'N/A')}")
        click.echo(f"Brand: {product.get('brand', 'N/A')}")
        click.echo(f"Category: {product.get('category', 'N/A')}")
        click.echo(f"Description: {product.get('description', 'N/A')}")
        if product.get('barcode'):
            click.echo(f"Barcode: {product['barcode']}")
        
        # Offer to add to inventory
        if click.confirm("\nDo you want to add this product to inventory?"):
            price = click.prompt("Enter price", type=float)
            quantity = click.prompt("Enter quantity", type=int)
            add_data = {
                'name': product['name'],
                'price': price,
                'quantity': quantity,
                'brand': product.get('brand'),
                'category': product.get('category'),
                'description': product.get('description'),
                'barcode': product.get('barcode')
            }
            add_result = InventoryCLI.make_request('POST', '/inventory', add_data)
            if add_result and add_result.get('status') == 'success':
                click.echo("Product added to inventory successfully!")
        click.echo(f"{'='*50}")
    elif result:
        click.echo(f"Error: {result.get('message', 'Product not found')}")

if __name__ == '__main__':
    cli()