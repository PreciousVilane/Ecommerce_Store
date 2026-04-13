from django.shortcuts import render
from store.models import Product, Store

""" For home page since it doesnt belong to a specific app """


def home(request):
    products = Product.objects.all()  # get all products
    stores = Store.objects.all()  # get all stores

    context = {
        "products": products,
        "stores": stores,
    }

    return render(request, "home.html", context)
