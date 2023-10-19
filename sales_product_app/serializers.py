from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import Shop, Category, UserInfo


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = ('company', 'position')


class UserRegistrationSerializer(UserCreateSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(max_length=100, required=True)
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)
    # company = UserInfoSerializer(required=True)
    # position = UserInfoSerializer(required=True)
    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'name')
#         read_only_fields = ('id',)
