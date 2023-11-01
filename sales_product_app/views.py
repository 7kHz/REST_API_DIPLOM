from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .models import ProductInfo, Shop, Category, Product, Parameter, ProductParameter, Order, OrderList
from .serializers import ProductInfoSerializer, ShopSerializer, CategorySerializer, ProductSerializer, \
    OrderSerializer, OrderListSerializer


# Create your views here.

def account_activation(request, uid, token):
    context = {
        'uid': uid,
        'token': token
    }
    return render(request, 'account_activation.html', context)


def create_order(user_id, product_info_id, product):
    order_count = Order.objects.filter(product_info_id=product_info_id).count()
    if order_count >= 1:
        return Response(f"{product} уже в корзине")
    Order.objects.create(user_id=user_id, product_info_id=product_info_id)
    return Response(f"{product} добавлен в Корзину")




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


# class ProductInfoViewSet(viewsets.ModelViewSet):
#     queryset = ProductInfo.objects.all()
#     serializer_class = ProductInfoSerializer
#     filter_backends = [OrderingFilter]
#     ordering_fields = ['retail_price']
#     permission_classes = [IsAuthenticatedOrReadOnly]


class ProductInfoView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, product_id):
        product_info = ProductInfo.objects.get(product_id=product_id)

        return Response(ProductInfoSerializer(product_info).data)

    def put(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        if not product_id:
            return Response({'Error': 'Method PUT not allowed'})
        try:
            instance = ProductInfo.objects.get(product_id=product_id)
        except:
            return Response({'Error': 'Object does not exists'})
        serializer = ProductInfoSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if serializer.data['basket']:
            return create_order(request.user.id, serializer.data['id'], serializer.data['product'])
        return Response(serializer.data)


class BasketView(ListCreateAPIView):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
