from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import Shop, Category, CustomUser, ProductInfo, Product, Parameter, ProductParameter, Order, OrderList


class CustomUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name',
                  'company', 'position', 'type')


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


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.StringRelatedField()
    url = serializers.HyperlinkedIdentityField(view_name="product-detail")

    class Meta:
        model = Product
        fields = ('url', 'name', 'category')


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


class ProductInfoSerializer(serializers.HyperlinkedModelSerializer):
    shop = serializers.StringRelatedField()
    product_parameter = ProductParameterSerializer(read_only=True, many=True)
    product = serializers.StringRelatedField()
    basket = serializers.BooleanField(required=True)
    quantity = serializers.IntegerField(required=False)
    retail_price = serializers.IntegerField(required=False)

    # basket = serializers.HyperlinkedIdentityField(view_name='productinfo-detail', lookup_field='product_id')

    # url = serializers.HyperlinkedIdentityField(view_name='productinfo-detail', lookup_field='product_id')

    class Meta:
        model = ProductInfo
        fields = ('id', 'product_id', 'product', 'shop', 'quantity', 'retail_price', 'product_parameter', 'basket')


class OrderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    shop = serializers.CharField(max_length=50)
    price = serializers.IntegerField(min_value=0)
    sum_value = serializers.IntegerField(min_value=0)

    class Meta:
        model = Order
        fields = ('id', 'name', 'shop', 'price', 'quantity', 'sum_value')

    def update(self, instance, validated_data):
        pass


class OrderQuantityUpdateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)
    # product_info = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=True, min_value=1)

    class Meta:
        model = Order
        fields = ('id', 'user', 'quantity')


class OrderListSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=True)

    class Meta:
        model = OrderList
        fields = ()
