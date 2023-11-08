from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import F, Sum, Count
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView, \
    RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from .models import CustomUser, ProductInfo, Shop, Category, Product, Order, Contact
from .serializers import ProductInfoSerializer, ShopSerializer, CategorySerializer, ProductSerializer, \
    BasketSerializer, ContactSerializer, ThanksForOrderSerializer, OrderListSerializer, OrderDetailSerializer


# Create your views here.

def account_activation(request, uid, token):
    context = {
        'uid': uid,
        'token': token
    }
    return render(request, 'account_activation.html', context)


class ShopView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            shops = Shop.objects.filter(pk=pk)
            return Response(ShopSerializer(shops, many=True).data)
        shops = Shop.objects.all()
        return Response(ShopSerializer(shops, many=True).data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'Error': 'Method PUT not allowed'})
        try:
            instance = Shop.objects.get(pk=pk)
        except:
            return Response({'Error': 'Object does not exists'})
        serializer = ShopSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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


class ProductInfoView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create_order(self, user_id, product_info_id, product):
        order_count = Order.objects.filter(user_id=user_id, product_info_id=product_info_id).count()
        if order_count >= 1:
            return Response(f"{product} уже в Корзине Пользователя (user_id: {user_id})")
        Order.objects.create(user_id=user_id, product_info_id=product_info_id)
        return Response(f"{product} добавлен в Корзину Пользователя (user_id: {user_id})")

    def get(self, request, product_id):
        if not product_id:
            return Response({'Error': 'Method GET not allowed'})
        try:
            product_info = ProductInfo.objects.get(product_id=product_id)
        except:
            return Response({'Error': 'Object does not exists'})
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
            return self.create_order(request.user.id, serializer.data['id'], serializer.data['product'])
        return Response(serializer.data)


class BasketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return Response({'Error': 'Method GET not allowed'})
        queryset = Order.objects.filter(user_id=request.user.id).select_related('product_info')
        queryset = queryset.annotate(name=F('product_info__name'),
                                     shop=F('product_info__shop__name'),
                                     price=F('product_info__retail_price'),
                                     quantity_in_stock=F('product_info__quantity_in_stock'),
                                     sum_value=Sum(F('product_info__retail_price') * F('quantity')))
        return Response(BasketSerializer(queryset, many=True).data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response("{'Error': 'Method PUT not allowed'}")
        try:
            instance = Order.objects.filter(user_id=request.user.id).get(pk=pk)
        except:
            return Response('Object does not exist')
        serializer = BasketSerializer(data=request.data, instance=instance)
        try:
            if int(request.data['quantity']) > instance.product_info.quantity_in_stock:
                return Response(f"Данное число превышает количество товара '{instance.product_info.name}' на складе")
        except KeyError:
            return Response({'Error': 'Введите число для изменения количества товара'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(f"Количество товара '{instance.product_info.name}' изменено на "
                        f"{serializer.data['quantity']} шт.")

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response("{'Error': 'Method DELETE not allowed'}")
        try:
            instance = Order.objects.filter(user_id=request.user.id).get(pk=pk)
        except:
            return Response('Object does not exist')
        instance.delete()
        return Response(f'Товар {instance.product_info.name} удален из Корзины')


class ContactView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return Response({'Error': 'Method GET not allowed'})
        queryset = Contact.objects.filter(user_id=request.user.id)
        return Response(ContactSerializer(queryset, many=True).data)

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return Response({'Error': 'Method POST not allowed'})
        contact_count = Contact.objects.filter(user_id=request.user.id).count()
        if contact_count >= 1:
            return Response('Количество адресов не может быть более 1')
        data = {'user': request.user.id}
        for key, value in request.data.items():
            value = str(value)
            data[key] = value
        serializer = ContactSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        OrderListView.update_order_new(self, self.request.user.id)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response("{'Error': 'Method PUT not allowed'}")
        try:
            instance = Contact.objects.filter(user_id=request.user.id).get(pk=pk)
        except:
            return Response('Object does not exist')
        serializer = ContactSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response("{'Error': 'Method DELETE not allowed'}")
        try:
            instance = Contact.objects.filter(user_id=request.user.id).get(pk=pk)
        except:
            return Response('Object does not exist')
        OrderListView.update_order_canceled(self, request.user.id)
        instance.delete()
        return Response(f'Контактные данные {instance.user} успешно удалены')


class ThanksForOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return Response("{'Error': 'Method GET not allowed'}")
        current_date = datetime.now().date()
        product_info = Order.objects.filter(user_id=request.user.id, status='new',
                                            date=current_date).select_related('product_info')
        product_info = product_info.annotate(name=F('product_info__name'),
                                             shop=F('product_info__shop__name'),
                                             price=F('product_info__retail_price'),
                                             sum_value=Sum(F('product_info__retail_price') * F('quantity')),
                                             email=F('user__email'),
                                             phone=F('user__contacts__phone'),
                                             street=F('user__contacts__street'),
                                             house=F('user__contacts__house'))
        return Response(ThanksForOrderSerializer(product_info, many=True).data)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['status']

    def update_order_new(self, user_id):
        Order.objects.filter(user_id=user_id, status='basket').update(status='new')
        orders = Order.objects.filter(user_id=user_id, status='new').values('user_id', 'date').annotate().distinct()
        for i, v in enumerate(orders):
            v['id'] = i + 1
            Order.objects.filter(user_id=v['user_id'], date=v['date']). \
                update(order_number=f"{user_id}-{v['id']}")

    def update_order_canceled(self, user_id):
        try:
            Order.objects.filter(user_id=user_id).exclude(status='basket').update(status='canceled')
        except:
            return Response('Object does not exist')

    def get(self, request, **kwargs):
        order_number = kwargs.get('order_number')
        if order_number:
            order = Order.objects.filter(user_id=request.user.id, order_number=order_number). \
                annotate(name=F('product_info__name'),
                         shop=F('product_info__shop__name'),
                         price=F('product_info__retail_price'),
                         sum_=Sum(F('product_info__retail_price') * F('quantity')),
                         email=F('user__email'),
                         phone=F('user__contacts__phone'),
                         street=F('user__contacts__street'),
                         house=F('user__contacts__house'))
            return Response(OrderDetailSerializer(order, many=True).data)
        orders = Order.objects.filter(user_id=request.user.id).values('user_id', 'date', 'status', 'order_number'). \
            annotate(sum_=Sum(F('product_info__retail_price') * F('quantity'))).distinct()
        return Response(OrderListSerializer(orders, many=True).data)


class ShopUpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        if request.user.type != 'supplier':
            return Response({'Error': 'Only for suppliers'})
        try:
            response = {}
            suppliers = CustomUser.objects.filter(type='supplier').values('id', 'username', 'company')
            for supplier in suppliers:
                Shop.objects.filter(name=supplier['company']).update(user_id=supplier['id'])
                response[f"Поставщик (username: '{supplier['username']}') прикреплен к магазину"] = \
                    f"{Shop.objects.filter(name=supplier['company'])[0]}"
            return Response(response)
        except:
            return Response({'Error': 'Supplier or Shop does not exists'})


class SupplierOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        order_number = kwargs.get('order_number')
        if request.user.type != 'supplier':
            return Response({'Error': 'Only for suppliers'})
        if order_number:
            try:
                order = Order.objects.filter(order_number=order_number).annotate(name=F('product_info__name'),
                                                                                 price=F('product_info__price'))
                return Response(OrderDetailSerializer(order, many=True).data)
            except:
                return Response('Object does not exist')
        order = Order.objects.filter(product_info__shop__user_id=request.user.id). \
            select_related('product_info__shop').exclude(status='Basket'). \
            annotate(sum_=Sum(F('product_info__price') * F('quantity')))
        return Response(OrderListSerializer(order, many=True).data)
