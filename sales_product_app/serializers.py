from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import Shop, Category, CustomUser, ProductInfo, Product, Parameter, ProductParameter


class CustomUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'company', 'position', 'type')


# class ProductInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductInfo
#         fields = ('__all__')


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'url', 'status')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category')


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('name',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    # product_info = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value')


# class BasketUrlSerializer(serializers.HyperlinkedModelSerializer):
#     product = serializers.StringRelatedField()
#     class Meta:
#         model = ProductInfo
#         fields = ('url',)


class ProductInfoSerializer(serializers.HyperlinkedModelSerializer):
    shop = serializers.StringRelatedField()
    product_parameter = ProductParameterSerializer(read_only=True, many=True)
    product = serializers.StringRelatedField()
    class Meta:
        model = ProductInfo
        fields = ('id', 'url', 'product', 'shop', 'quantity', 'retail_price', 'product_parameter')
