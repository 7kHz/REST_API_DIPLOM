import yaml
from django.core.management import BaseCommand
from django.db.models import F

from sales_product_app.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


class Command(BaseCommand):
    help = 'Load data from a YAML file into the database'

    def add_arguments(self, parser):
        parser.add_argument('yaml_file', type=str)

    def handle(self, *args, **options):
        try:
            with open('fixtures/shop1.yaml', 'r', encoding='utf8') as file:
                data = yaml.safe_load(file)
            for shop in data['shop']:
                Shop.objects.get_or_create(id=shop['id'], name=shop['name'], url=shop['url'])
            svyaznoy = Shop.objects.get(pk=1)
            mvideo = Shop.objects.get(pk=2)
            for category in data['categories']:
                Category.objects.get_or_create(id=category['id'], name=category['name'])
            smartphones, accessories, flash_storage = Category.objects.filter(id__in=[224, 15, 1])
            # Category.objects.get_or_create(id=4, name='Бытовая техника')
            # home_appliances = Category.objects.all()[3]
            smartphones.shops.set([svyaznoy])
            accessories.shops.set([svyaznoy])
            flash_storage.shops.set([mvideo])
            # home_appliances.shops.add(mvideo)
            for product in data['goods']:
                Product.objects.get_or_create(id=product['id'],
                                              category_id=product['category'],
                                              name=product['name'])
                # for shop in Product.objects.values(shop_id=F('category__shops__id')):
                ProductInfo.objects.get_or_create(product_id=product['id'],
                                                  shop_id=1,
                                                  name=product['name'],
                                                  quantity=product['quantity'],
                                                  price=product['price'],
                                                  retail_price=product['price_rrc'])
                for key, value in product['parameters'].items():
                    Parameter.objects.get_or_create(name=key)
                    ProductParameter.objects.create(parameter_id=Parameter.objects.get(name=key).id,
                                                    product_info_id=ProductInfo.objects.get(name=product['name']).id,
                                                    value=value)
        except yaml.YAMLError as error:
            print(error)
