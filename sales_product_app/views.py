from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView

from .serializers import CustomUser


# Create your views here.
class UsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUser
    # authentication_classes = (TokenAuthentication, )