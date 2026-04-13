from django.urls import path
from .views import create_store, vendor_stores, edit_store, delete_store
from .views import create_product, vendor_products, edit_product
from .views import delete_product
from .views import basic_api_response, view_stores

urlpatterns = [
    # VENDORS STORE URLS
    path("stores/", vendor_stores, name="vendor_stores"),
    path("stores/create/", create_store, name="create_store"),
    path("stores/edit/<int:store_id>/", edit_store, name="edit_store"),
    path("stores/delete/<int:store_id>/", delete_store, name="delete_store"),
    # VENDORS PRODUCTS URLS
    path("products/", vendor_products, name="vendor_products"),
    path("products/create/", create_product, name="create_product"),
    path("products/edit/<int:product_id>/", edit_product, name="edit_product"),
    path("products/delete/<int:product_id>/", delete_product, name="delete_product"),
    # API
    path("basic_response/", basic_api_response),
    path("get/stores", view_stores),
]
