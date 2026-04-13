from django.contrib import admin
from .models import Store, Product

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "quantity"]


admin.site.register(Store)  # now store can show on admin panel
admin.site.register(
    Product, ProductAdmin
)  # also products will show wiith the above list
