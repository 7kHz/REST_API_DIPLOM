from rest_framework import serializers
from .models import CustomUser, Shop, Category


# class UserSerializer(serializers.ModelSerializer):
#     type = serializers.CharField(read_only=True)
#
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'first_name', 'last_name', 'email', 'type')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)