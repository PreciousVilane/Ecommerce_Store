from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Order, OrderItem
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

""" ********** CART FUNCTIONALITY *********"""


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get existing cart from session or create empty
    cart = request.session.get("cart", {})

    # Increment quantity if already in cart
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    # Save back to session
    request.session["cart"] = cart
    messages.success(request, f" {product.name} was added to your cart.")

    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})
    items = []

    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        items.append(
            {
                "product": product,
                "quantity": quantity,
            }
        )
        total += product.price * quantity

    return render(request, "orders/cart.html", {"items": items, "total": total})


# remove item from cart


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart
    return redirect("cart")


""" ********** ORDERS FUNCTIONALITY *********"""


@login_required(login_url="login")
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("cart")

    # Prepare order items and total
    total_price = 0
    order_items_data = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        line_total = product.price * quantity
        total_price += line_total
        order_items_data.append(
            {
                "product": product,
                "quantity": quantity,
                "price": product.price,
                "line_total": line_total,
            }
        )

    if request.method == "POST":
        # Create order and order items
        order = Order.objects.create(
            user=request.user, total_price=total_price, status="completed"
        )

        for item in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["price"],
            )

        # Build email
        message_lines = [
            f"{item['product'].name} x {item['quantity']} = R{item['line_total']:.2f}"
            for item in order_items_data
        ]
        message = (
            f"Thank you for your purchase!\n\n"
            + "\n".join(message_lines)
            + f"\n\nTotal: R{total_price:.2f}"
        )

        html_message = render_to_string(
            "orders/invoice_email.html",
            {
                "user": request.user,
                "order": order,
                "order_items": order_items_data,
                "total_price": total_price,
            },
        )

        # Send email
        send_mail(
            subject=f"Invoice for your order #{order.id}",
            message=message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com"),
            recipient_list=[request.user.email],
            html_message=html_message,
        )

        # Clear cart
        request.session["cart"] = {}

        # Render success page
        return render(request, "orders/checkout_success.html", {"order": order})

    # GET request → just show checkout summary
    return render(
        request,
        "orders/checkout.html",
        {"order_items": order_items_data, "total_price": total_price},
    )
