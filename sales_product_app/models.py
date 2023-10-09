from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)


class Shop(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    url = models.URLField(blank=True, null=True)
    filename = models.CharField(max_length=30, unique=True, blank=True, verbose_name='Имя_файла')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название')
    shops = models.ManyToManyField(Shop, related_name='shops_categories', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название')
    category = models.ForeignKey(Category, blank=True, verbose_name='Категории',
                                 related_name='product_category', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    retail_price = models.PositiveIntegerField(verbose_name='Розничная цена')
    product = models.ForeignKey(Product, blank=True, verbose_name='Продукты',
                                related_name='productinfo_product', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, blank=True, verbose_name='Магазины',
                             related_name='productinfo_shop', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт_инфо'
        verbose_name_plural = 'Продукты_инфо'

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    value = models.BooleanField(verbose_name='Статус')
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте',
                                     related_name='productparametr_product_info', on_delete=models.CASCADE)
    parameter = models.ForeignKey('Parameter', verbose_name='Параметр',
                                  related_name='productparameter_parameter', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Параметр продукта'
        verbose_name_plural = 'Параметры продуктов'


class Parameter(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = 'Имена параметров'

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    shop = models.ForeignKey(Shop, blank=True, verbose_name='Магазины',
                             related_name='orderitem_shop', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, verbose_name='Продукты',
                                related_name='orderitem_product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', blank=True, verbose_name='Заказ',
                              related_name='orderitem_order', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = 'Список заказанных позиций'


class Order(models.Model):
    date = models.DateField(verbose_name='Дата заказа', auto_now_add=True)
    status = models.Field(choices=STATE_CHOICES, verbose_name='Статус')
    user = models.ForeignKey(User, blank=True, verbose_name='Пользователь',
                             related_name='order_user', on_delete=models.CASCADE)


class Contact(models.Model):
    type = models.CharField(max_length=30, unique=True, verbose_name='Тип')
    value = models.CharField(max_length=30, unique=True, verbose_name='Значение')
    user = models.ForeignKey(User, blank=True, verbose_name='Пользователь',
                             related_name='contact_user', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Контакты пользователей'
        verbose_name_plural = 'Список контактов пользователей'

    def __str__(self):
        return self.value
