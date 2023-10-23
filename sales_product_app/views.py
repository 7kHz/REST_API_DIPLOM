from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProductInfo, Shop, Category
from .serializers import ProductInfoSerializer, ShopSerializer, CategorySerializer


# Create your views here.

def account_activation_success(request, uid, token):
    try:
        # if request.user.is_authenticated:
        # user = get_object_or_404(get_user_model(), id=request.user.id)
        # username = user.username
        if token and uid:
            return render(request, 'account_activation_success.html')
    except Http404:
        return render(request, 'account_activation_error.html')


class ProductInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            queryset = ProductInfo.objects.filter(pk=pk)
        else:
            queryset = ProductInfo.objects.all()
        serializer = ProductInfoSerializer(queryset, many=True)
        return Response(serializer.data)


class ShopView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
