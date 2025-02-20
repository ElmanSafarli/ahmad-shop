from django.urls import path
from .views import cart_add, cart_summary

app_name = 'shop_cart'

urlpatterns = [
    path('', cart_summary, name='cart_summary'),
    path('add/', cart_add, name='cart_add'),
]
