from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView

from .models import UserInfo
from .serializers import UserInfoSerializer, UserRegistrationSerializer


# Create your views here.

class UserInfoView(ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    # def perform_create(self, serializer):
    #     user_id = self.request.data.get('user_id')
    #     user = User.objects.get(pk=user_id)
    #     serializer.save(user=user)
        # UserInfo.objects.create(user_id=user_id, company=company, position=position )
        # serializer.save()



# class UsersView(ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = CustomUser
# authentication_classes = (TokenAuthentication, )
