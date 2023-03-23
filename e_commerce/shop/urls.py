from django.contrib import admin
from django.urls import path
from shop.views import *

urlpatterns = [
    path('shop/', shop.as_view(),name="shop"),
    path('add_to_cart/<id>', add_to_cart,name="add_to_cart"),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('remove_cart/<id>/', remove_cart,name = "remove_cart"),
    path('cart/', cart_view.as_view(), name='cart'),
    path('checkout_address/', CheckoutAddress.as_view(), name='checkout_address'),
    path('checkout_payment/', CheckoutPayment.as_view(), name='checkout_payment'),
    path('update_cart', UpdateCart, name='update_cart')
    # path('checkout/success/', checkout_success, name='checkout_success'),
]
