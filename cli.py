#!/usr/bin/env python3
"""
Command Line Interface for Inventory Management System
"""

import click
import requests

API_BASE_URL = "http://localhost:5000"

class InventoryCLI:
    @staticmethod
    def make_request(method, endpoint, data=None):
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
            click.echo("\nError: Cannot connect to API server. Make sure it's running: python run.py\n")
            return None
        except requests.exceptions.RequestException as e:
            click.echo(f"Error: {e}")
            return None

    @staticmethod
    def format_item(item):
        click.echo(f"ID: {item['id']}")
        click.echo(f"Name: {item['name']}")
        click.echo(f"Price: ${item['price']:.2f}")
        click.echo(f"Quantity: {item['quantity']}")
        if item.get('brand'):
            click.echo(f"Brand: {item['brand']}")
        if item.get('description'):
            click.echo(f"Description: {item['description'][:100]}")
        if item.get('barcode'):
            click.echo(f"Barcode: {item['barcode']}")
        click.echo("")

@click.group()
def cli():
    pass

@cli.command()
def list():
    result = InventoryCLI.make_request('GET', '/inventory')
    if result and result.get('status') == 'success':
        items = result.get('data', [])
        if items:
            click.echo(f"\nTotal items: {len(items)}\n")
            for item in items:
                InventoryCLI.format_item(item)
        else:
            click.echo("\nNo items in inventory\n")

@cli.command()
@click.argument('item_id', type=int)
def view(item_id):
    result = InventoryCLI.make_request('GET', f'/inventory/{item_id}')
    if result and result.get('status') == 'success':
        click.echo("")
        InventoryCLI.format_item(result['data'])
    elif result:
        click.echo(f"Error: {result.get('message', 'Item not found')}")

@cli.command()
@click.option('--name', prompt='Product name')
@click.option('--price', prompt='Price', type=float)
@click.option('--quantity', prompt='Quantity', type=int)
@click.option('--brand', help='Product brand')
@click.option('--description', help='Product description')
@click.option('--barcode', help='Product barcode')
def add(name, price, quantity, brand, description, barcode):
    data = {'name': name, 'price': price, 'quantity': quantity}
    if brand: data['brand'] = brand
    if description: data['description'] = description
    if barcode: data['barcode'] = barcode
    result = InventoryCLI.make_request('POST', '/inventory', data)
    if result and result.get('status') == 'success':
        click.echo(f"\nSuccess: {result['message']}\n")
        InventoryCLI.format_item(result['data'])

@cli.command()
@click.argument('item_id', type=int)
@click.option('--name', help='Product name')
@click.option('--price', type=float, help='Product price')
@click.option('--quantity', type=int, help='Stock quantity')
@click.option('--brand', help='Product brand')
@click.option('--description', help='Product description')
def update(item_id, name, price, quantity, brand, description):
    data = {}
    if name: data['name'] = name
    if price is not None: data['price'] = price
    if quantity is not None: data['quantity'] = quantity
    if brand: data['brand'] = brand
    if description: data['description'] = description
    if not data:
        click.echo("No fields to update")
        return
    result = InventoryCLI.make_request('PATCH', f'/inventory/{item_id}', data)
    if result and result.get('status') == 'success':
        click.echo(f"\nSuccess: {result['message']}\n")
        InventoryCLI.format_item(result['data'])

@cli.command()
@click.argument('item_id', type=int)
def delete(item_id):
    click.confirm(f"Are you sure you want to delete item {item_id}?", abort=True)
    result = InventoryCLI.make_request('DELETE', f'/inventory/{item_id}')
    if result and result.get('status') == 'success':
        click.echo(f"\nSuccess: {result['message']}\n")

@cli.command()
@click.option('--barcode', help='Product barcode')
@click.option('--name', help='Product name')
def find(barcode, name):
    if not barcode and not name:
        click.echo("Please provide either --barcode or --name")
        return
    params = []
    if barcode: params.append(f"barcode={barcode}")
    if name: params.append(f"name={name}")
    result = InventoryCLI.make_request('GET', f'/external/product?{"&".join(params)}')
    if result and result.get('status') == 'success':
        product = result['data']
        click.echo("\nProduct found:")
        click.echo(f"Name: {product.get('name', 'N/A')}")
        click.echo(f"Brand: {product.get('brand', 'N/A')}")
        click.echo(f"Category: {product.get('category', 'N/A')}")
        desc = product.get('description', 'N/A')
        click.echo(f"Description: {desc[:200]}")
        if product.get('barcode'): click.echo(f"Barcode: {product['barcode']}")
        if click.confirm("\nDo you want to add this product to inventory?"):
            price = click.prompt("Enter price", type=float)
            quantity = click.prompt("Enter quantity", type=int)
            add_data = {
                'name': product['name'],
                'price': price,
                'quantity': quantity,
                'brand': product.get('brand'),
                'description': product.get('description'),
                'barcode': product.get('barcode')
            }
            add_result = InventoryCLI.make_request('POST', '/inventory', add_data)
            if add_result and add_result.get('status') == 'success':
                click.echo("\nProduct added to inventory successfully!")
    elif result:
        click.echo(f"Error: {result.get('message', 'Product not found')}")

if __name__ == '__main__':
    cli()
