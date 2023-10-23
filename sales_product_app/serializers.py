from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import Shop, Category, CustomUser, ProductInfo


# class CustomUserPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
#     def to_internal_value(self, data):
#         try:
#             user_id = int(data)
#             return get_user_model().objects.get(pk=user_id)
#         except(ValueError, get_user_model().DoesNotExist):
#             raise serializers.ValidationError('Invalid user ID')
#
#
# class CustomUserActivationSerializer(UserCreateSerializer):
#     uid = CustomUserPrimaryKeyRelatedField(queryset=get_user_model().objects.all(), write_only=True)


class CustomUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'company', 'position', 'type')


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ('__all__')


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name', 'url', 'status')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
