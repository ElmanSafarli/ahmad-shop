from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.http import JsonResponse
from .cart import Cart

def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product)

        response = JsonResponse({'Product Name: ': product.name})

        return response