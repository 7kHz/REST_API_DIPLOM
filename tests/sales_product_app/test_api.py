import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from sales_product_app.models import Shop, Product, ProductInfo, Category, CustomUser


@pytest.fixture
def client(get_auth_token):
    auth_client = APIClient()
    auth_client.credentials(HTTP_AUTHORIZATION=f'Token {get_auth_token}')
    return auth_client


@pytest.fixture
def shop_factory():
    def factory(*args, **kwargs):
        return baker.make(Shop, *args, **kwargs)

    return factory


@pytest.fixture
def category_factory():
    def factory(*args, **kwargs):
        return baker.make(Category, *args, **kwargs)

    return factory


@pytest.fixture
def product_factory():
    def factory(*args, **kwargs):
        return baker.make(Product, *args, **kwargs)

    return factory


@pytest.fixture
def product_info_factory():
    def factory(*args, **kwargs):
        return baker.make(ProductInfo, *args, **kwargs)

    return factory


@pytest.fixture
def get_auth_token(client):
    data = {
        'username': 'testuser',
        'email': 'example@ya.ru',
        'password': 'testpassword',
    }
    CustomUser.objects.create_user(username=data['username'], email=data['email'],
                                   password=data['password'], type='supplier', is_active=True)
    login_data = {
        'username': data['username'],
        'email': data['email'],
        'password': data['password'],
    }
    response = client.post('/auth/token/login/', data=login_data)
    return response.data.get('auth_token')


@pytest.mark.django_db
def test_update_product(client, category_factory, product_factory):
    categories = category_factory(_quantity=3)
    product_factory(category_id=categories[0].id, _quantity=3)
    response = client.put('/api/v1/products/2/', data={'name': 'Kingston DataTraveler Exodia Onyx 64GB USB3.2 Black'})
    assert response.status_code == 200
    assert response.data['name'] == 'Kingston DataTraveler Exodia Onyx 64GB USB3.2 Black'


@pytest.mark.django_db
def test_shop_update(client, shop_factory):
    shop_factory(_quantity=3)
    response = client.put('/api/v1/shops/1/', data={'name': 'DNS', 'url': 'https://www.dns-shop.ru'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_shop(client, shop_factory):
    shop = shop_factory(_quantity=3)
    response = client.get('/api/v1/shops/')
    assert response.status_code == 200
    for i, v in enumerate(response.data):
        assert v['name'] == shop[i].name


@pytest.mark.django_db
def test_product_info(client, category_factory, product_factory, product_info_factory):
    categories = category_factory(_quantity=3)
    products = product_factory(category_id=categories[0].id, _quantity=3)
    for product in products:
        product_info_factory(product_id=product.id)
        URL = reverse('productinfo-detail', args=[product.id])
        response = client.get(URL)
        assert response.status_code == 200
        assert response.data['product'] == product.name
