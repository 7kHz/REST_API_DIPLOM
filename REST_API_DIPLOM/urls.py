"""
URL configuration for REST_API_DIPLOM project.

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
from django.urls import path, include, re_path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from sales_product_app.views import ProductInfoView, ShopView, CategoryView, account_activation_success


# from sales_product_app.views import UserInfoView

# router = DefaultRouter()
# router.register('users', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^auth/', include('djoser.urls.authtoken'), name='token-login-logout'),
    path('api/v1/', include('djoser.urls'), name='user-create-password-reset'),
    path('api/v1/product/<int:pk>/', ProductInfoView.as_view(), name='product-detail'),
    path('api/v1/product/', ProductInfoView.as_view(), name='product-list'),
    path('api/v1/shops/', ShopView.as_view(), name='shops-list'),
    path('api/v1/categories/', CategoryView.as_view(), name='category-list'),
    path('activate/<str:uid>/<str:token>/', account_activation_success, name='account_activation_success')


]
