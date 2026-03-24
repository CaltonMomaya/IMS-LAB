import requests
from typing import Dict, Optional

class OpenFoodFactsService:
    """Service to interact with OpenFoodFacts API"""
    
    BASE_URL = "https://world.openfoodfacts.org/api/v0/product"
    
    @staticmethod
    def fetch_product_by_barcode(barcode: str) -> Optional[Dict]:
        """
        Fetch product details from OpenFoodFacts by barcode
        
        Args:
            barcode: Product barcode string
            
        Returns:
            Dictionary with product information or None if not found
        """
        try:
            response = requests.get(f"{OpenFoodFactsService.BASE_URL}/{barcode}.json")
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 1 and data.get('product'):
                product_data = data['product']
                return {
                    'name': product_data.get('product_name', 'Unknown'),
                    'brand': product_data.get('brands', 'Unknown'),
                    'description': product_data.get('ingredients_text', 'No description available'),
                    'category': product_data.get('categories', 'Uncategorized'),
                    'barcode': barcode,
                    'price': None,  # Price not provided by API
                    'quantity': 0   # Quantity not provided by API
                }
            return None
            
        except requests.RequestException as e:
            print(f"Error fetching product: {e}")
            return None
    
    @staticmethod
    def search_product_by_name(product_name: str) -> Optional[Dict]:
        """
        Search for product by name in OpenFoodFacts
        
        Args:
            product_name: Name of product to search
            
        Returns:
            First matching product or None
        """
        try:
            search_url = "https://world.openfoodfacts.org/cgi/search.pl"
            params = {
                'search_terms': product_name,
                'search_simple': 1,
                'action': 'process',
                'json': 1,
                'page_size': 1
            }
            
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('products') and len(data['products']) > 0:
                product = data['products'][0]
                return {
                    'name': product.get('product_name', 'Unknown'),
                    'brand': product.get('brands', 'Unknown'),
                    'description': product.get('ingredients_text', 'No description available'),
                    'category': product.get('categories', 'Uncategorized'),
                    'barcode': product.get('code', ''),
                    'price': None,
                    'quantity': 0
                }
            return None
            
        except requests.RequestException as e:
            print(f"Error searching product: {e}")
            return None