from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils import timezone

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('received', 'Получен'),
    ('canceled', 'Отменен'),
)

USER_TYPE_CHOICES = (
    ('supplier', 'Поставщик'),
    ('buyer', 'Покупатель'),

)


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)
#
#
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True, verbose_name='Пользователь')
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    company = models.CharField(max_length=50, verbose_name='Компания')
    position = models.CharField(max_length=30, verbose_name='Должность')
    type = models.CharField(max_length=10, verbose_name='Тип пользователя', choices=USER_TYPE_CHOICES, default='buyer')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    #
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)


class Shop(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    url = models.URLField(blank=True, max_length=100)
    filename = models.CharField(max_length=50, blank=True, verbose_name='Имя_файла')
    user = models.OneToOneField(CustomUser, max_length=50, verbose_name='Пользователь',
                                blank=True, null=True, on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Статус получения заказов', default=True)

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
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    category = models.ForeignKey(Category, blank=True, verbose_name='Категории',
                                 related_name='product_category', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    quantity_in_stock = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    retail_price = models.PositiveIntegerField(verbose_name='Розничная цена')
    product = models.ForeignKey(Product, blank=True, verbose_name='Продукты',
                                related_name='product_name', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, blank=True, null=True, verbose_name='Магазины',
                             related_name='productinfo_shop', on_delete=models.CASCADE)
    basket = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Продукт_инфо'
        verbose_name_plural = 'Продукты_инфо'

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    value = models.CharField(max_length=30, verbose_name='Значение', blank=True, null=True)
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте', blank=True, null=True,
                                     related_name='product_parameter', on_delete=models.CASCADE)
    parameter = models.ForeignKey('Parameter', verbose_name='Параметр', blank=True, null=True,
                                  related_name='parameter_name', on_delete=models.CASCADE)

    def __str__(self):
        return self.value

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

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = 'Список заказанных позиций'


class Order(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', related_name='orders', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата заказа', auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATE_CHOICES, verbose_name='Статус', default='basket')
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте',
                                     related_name='orders', on_delete=models.CASCADE)
    order_number = models.CharField(verbose_name='Номер заказа', blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Contact(models.Model):
    user = models.ForeignKey(CustomUser, blank=True, verbose_name='Пользователь',
                             related_name='contacts', on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=20, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=20, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=20, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=20, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакты пользователей'
        verbose_name_plural = 'Список контактов пользователей'

    def __str__(self):
        return f'{self.city} {self.street} {self.house}'
