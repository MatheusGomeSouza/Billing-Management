"""
URL configuration for BillingManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from django.contrib.auth import views as auth_views
from invoice import views as invoice_views

urlpatterns = [
    path('', invoice_views.index, name='index'),
    path('form/', invoice_views.form, name='form'),
    path('basic/', invoice_views.basic, name='basic'),
    path('billing/', invoice_views.billing, name='billing'),
    path('itens/<str:billing_id>/', invoice_views.item_form, name='itens'),
    path('post_itens/', invoice_views.itens, name='post_itens'),
    path('admin/', admin.site.urls),
]
