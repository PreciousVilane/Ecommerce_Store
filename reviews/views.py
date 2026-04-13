from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product
from .models import Review
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from orders.models import OrderItem


@login_required
def add_review(request, product_id):

    if not request.user.is_buyer:
        return HttpResponseForbidden("Only buyers can leave reviews.")

    product = get_object_or_404(Product, id=product_id)

    # CHECK IF USER PURCHASED THE PRODUCT
    has_purchased = OrderItem.objects.filter(
        order__user=request.user, order__status="completed", product=product
    ).exists()

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # Optional: prevent duplicate reviews
        if Review.objects.filter(user=request.user, product=product).exists():
            return HttpResponseForbidden("You already reviewed this product.")

        Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            comment=comment,
            verified=has_purchased,
        )

        return redirect("all_products")

    return render(request, "reviews/add_review.html", {"product": product})
