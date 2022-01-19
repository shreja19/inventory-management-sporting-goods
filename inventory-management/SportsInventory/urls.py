"""SportsInventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from admins import views as admins
from django.urls import path
from users import views as usr
from . import views as mainView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', mainView.index, name='index'),
    path('index/', mainView.index, name='index'),
    path("cust_reg/", mainView.cust_reg, name="cust_reg"),


#User Side Views
    path("UserRegisterActions/", usr.UserRegisterActions, name="UserRegisterActions"),
    path("UserLoginCheck/", usr.UserLoginCheck, name="UserLoginCheck"),
    path("UserHome/", usr.UserHome, name="UserHome"),
    path("user_search_by_category/", usr.user_search_by_category, name="user_search_by_category"),
    path("user_add_cart/", usr.user_add_cart, name="user_add_cart"),
    path("userCheckCartData/", usr.userCheckCartData, name="userCheckCartData"),
    path("user_check_out/", usr.user_check_out, name="user_check_out"),
    path("user_order_details/", usr.user_order_details, name="user_order_details"),
    path("get_purchase_list/", usr.get_purchase_list, name="get_purchase_list"),


#Admin Side Views
    path("AdminHome/", admins.AdminHome, name="AdminHome"),
    path("admin_products/", admins.admin_products, name='admin_products'),
    path("AdminUpdateProducts/", admins.AdminUpdateProducts, name="AdminUpdateProducts"),
    path("AdminDeleteProduct/", admins.AdminDeleteProduct, name="AdminDeleteProduct"),
    path("admin_products_update/", admins.admin_products_update, name="admin_products_update"),
    path('admin_view_orders/', admins.admin_view_orders, name="admin_view_orders"),
    path("admin_view_purchase_items/", admins.admin_view_purchase_items, name="admin_view_purchase_items"),

]