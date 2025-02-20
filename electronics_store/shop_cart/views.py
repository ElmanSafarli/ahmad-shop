from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.http import JsonResponse
from .cart import Cart

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    total_quantity = cart.get_total_quantity()

    return render(request, 'shop_cart/cart_summary.html', {'cart_products': cart_products,  'total_quantity': total_quantity})

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product)

        response = JsonResponse({'Product Name: ': product.name})

        return response
    
def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)

        response = JsonResponse({'Product Name: ': product_id})

        return response