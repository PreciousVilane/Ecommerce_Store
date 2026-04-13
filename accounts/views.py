from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import User

# from django.http import HttpResponse


# def home(request):
# return HttpResponse("Welcome to the Store App")


User = get_user_model()  # Works with your custom user model


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password_1 = request.POST.get("password1")
        password_2 = request.POST.get("password2")
        email = request.POST.get("email")
        role = request.POST.get("role")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # Create user with hashed password
        if password_1 == password_2:
            user = User.objects.create_user(
                username=username,
                password=password_1,
                email=email,
            )
        else:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        # Assign role
        if role == "vendor":
            user.is_vendor = True
        else:
            user.is_buyer = True

        user.save()  # Save the role changes

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")  # Redirect to login page

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # log the user in

            # Redirect based on role
            if user.is_vendor:
                return redirect("vendor_stores")
            elif user.is_buyer:
                return redirect("all_products")
            else:
                return redirect("home")

        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "accounts/login.html", {"username": username})

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
