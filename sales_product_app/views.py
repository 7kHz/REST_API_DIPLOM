from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .models import ProductInfo, Shop, Category, Product, Parameter, ProductParameter
from .serializers import ProductInfoSerializer, ShopSerializer, CategorySerializer, ProductSerializer, \
    ParameterSerializer, ProductParameterSerializer


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


class ShopView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['name']
    search_fields = ['name']
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductInfoViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['retail_price']
    permission_classes = [IsAuthenticatedOrReadOnly]


# class ProductInfoView(ListAPIView):
#     queryset = ProductInfo.objects.all()
#     serializer_class = BasketUrlSerializer
    # def get(self, request):
    #     queryset = ProductInfo.objects.all()
    #     serializer = BasketUrlSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)

