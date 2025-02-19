from django.urls import path
from .views import cart_add

app_name = 'shop_cart'

urlpatterns = [
    path('add/', cart_add, name='cart_add'),
]
