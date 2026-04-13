"""
URL configuration for Ecommerce_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf import settings
from django.conf.urls.static import static
from store.views import all_products

urlpatterns = [
    path("admin/", admin.site.urls),
    # For home page
    path("", home, name="home"),
    # Buyer products page (accessible to all, especially buyers)
    path("products/", all_products, name="all_products"),
    # Accounts app (handles /login/, /register/ etc.)
    path("accounts/", include("accounts.urls")),
    # Store app (handles /vendor/ etc.)
    path("vendor/", include("store.urls")),
    # Reviews app
    path("reviews/", include("reviews.urls")),
    # Orders app (cart, checkout)
    path("orders/", include("orders.urls")),
]

# for user uploads
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # For site related 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
