from django.urls import path
from .views import add_to_cart, cart_view, remove_from_cart
from .views import checkout

urlpatterns = [
    # CART URLS
    path("cart/", cart_view, name="cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", remove_from_cart, name="remove_from_cart"),
    # existing cart URLs...
    path("checkout/", checkout, name="checkout"),
]
