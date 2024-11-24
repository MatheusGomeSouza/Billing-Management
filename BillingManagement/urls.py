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
from user import views as user_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register', user_views.register, name='register'),
    path('', invoice_views.index, name='index'),
    path('form/', invoice_views.form, name='form'),
    path('preview/', invoice_views.basic_data, name='preview'),
    path('billing_view/', invoice_views.billing_view, name='billing_view'),
    path('basic/', invoice_views.basic, name='basic'),
    path('billing/', invoice_views.billing, name='billing'),
    path('itens/<str:billing_id>/', invoice_views.item_form, name='itens'),
    path('post_itens/', invoice_views.itens, name='post_itens'),
    path('post_investiment/', invoice_views.investiment, name='post_investiment'),
    path('accounts/profile/', invoice_views.rend, name='rend'),
    path('admin/', admin.site.urls),
]
