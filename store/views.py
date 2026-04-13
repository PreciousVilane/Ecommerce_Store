from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Store, Product

"""For API: """
from .functions.tweet import Tweet
from rest_framework import serializers, status
from django.http import JsonResponse
from .serializers import StoreSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

""" ********** VENDORS CRUD FUNTIONS & PERMISSIONS **********"""


@login_required
def create_store(request):
    # If the logged-in user is NOT a vendor, send them back to the home page
    if not request.user.is_vendor:
        return redirect("home")

    # Check if the form was submitted
    if request.method == "POST":

        # Get the store name and description from the form input
        name = request.POST.get("name")
        description = request.POST.get("description")
        print(description, name)

        # create & saving to database, using variable so we can call it again
        # for twitter
        store = Store.objects.create(
            owner=request.user, name=name, description=description
        )

        # new_store_tweet = f"New store open on Grabsomore!\n{store.name}\n\n{store.description}"
        # tweet = {'text': new_store_tweet}
        try:
            Tweet.tweet_new_store(store)
        except Exception as e:
            print("twitter error is: ", e)
        return HttpResponseRedirect(reverse("vendor_stores"))
    else:
        return render(request, "store/create_store.html")


# View vendor stores
@login_required
def vendor_stores(request):
    # If the logged-in user is NOT a vendor, send them back to the home page
    if not request.user.is_vendor:
        return redirect("home")

    stores = Store.objects.filter(owner=request.user)
    return render(request, "store/vendor_stores.html", {"stores": stores})


# Edit store
@login_required
def edit_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        store.name = request.POST.get("name")
        store.description = request.POST.get("description")
        store.save()
        return redirect("vendor_stores")

    return render(request, "store/edit_store.html", {"store": store})


# Delete store
@login_required
def delete_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        store.delete()
        return redirect("vendor_stores")

    return render(request, "store/delete_store.html", {"store": store})


""" ********** VENDORS PRODUCTS CRUD FUNTIONS & PERMISSIONS **********"""


# Create product
@login_required
def create_product(request):
    # If the logged-in user is NOT a vendor, send them back to the home page
    if not request.user.is_vendor:
        return redirect("home")

    stores = Store.objects.filter(owner=request.user)

    # Check if the form was submitted
    if request.method == "POST":
        store_id = request.POST.get("store")
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        product_image = request.FILES.get("image")

        store = get_object_or_404(Store, id=store_id, owner=request.user)

        product = Product.objects.create(
            store=store,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            product_image=product_image
        )

        # tweeting new product added
        try:
            Tweet.tweet_new_product(product)
        except Exception as e:
            print("Twitter error:", e)

        return redirect("vendor_products")

    return render(request, "store/create_product.html", {"stores": stores})


# View product
@login_required
def vendor_products(request):
    # If the logged-in user is NOT a vendor, send them back to the home page

    if not request.user.is_vendor:
        return redirect("home")

    products = Product.objects.filter(store__owner=request.user)
    return render(request, "store/vendor_products.html", {"products": products})


# Edit product
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, store__owner=request.user)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.quantity = request.POST.get("quantity")
        product.save()
        return redirect("vendor_products")
    if request.FILES.get("image"):
        product.product_image = request.FILES.get("image")

    return render(request, "store/edit_product.html", {"product": product})


# Delete product
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, store__owner=request.user)

    if request.method == "POST":
        product.delete()
        return redirect("vendor_products")

    return render(request, "store/delete_product.html", {"product": product})


""" ********** Buyers Products ********** """


def all_products(request):
    products = Product.objects.all()
    return render(request, "store/products.html", {"products": products})


""" ********** API FUNCTIONALITY ********** """


def basic_api_response(request):
    if request.method == "GET":
        data = serializers.serialize("json", Store.objects.all())
        return JsonResponse(data=data, safe=False)


@api_view(["GET"])
@renderer_classes((XMLRenderer,))
def view_stores(request):
    if request.method == "GET":
        serializer = StoreSerializer(Store.objects.all(), many=True)
        return Response(data=serializer.data)


@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_stores(request):
    if request.method == "POST":
        if request.user.id == request.data["vendor"]:
            # getting requested POST turn it into data then serialize it
            serializer = StoreSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(
                    data=serializer.data, status=status.HTTP_201_CREATED
                )
            # error handling
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(
            {"ID mismatch": "User ID and store ID not matching"},
            status=status.HTTP_400_BAD_REQUEST,
        )
