from products.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')
        
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 1
            }
        else:
            self.cart[product_id]['quantity'] += 1
        
        self.session.modified = True

    
    def get_prods(self):
        products_ids = [int(pid) for pid in self.cart.keys()] 
        products = Product.objects.filter(id__in=products_ids)

        return products
    
    def get_total_quantity(self):
        """Returns the total quantity of items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())