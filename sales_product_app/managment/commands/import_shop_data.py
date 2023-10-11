import yaml
from django.core.management import BaseCommand
from REST_API_DIPLOM.sales_product_app.models import Shop, Category


class Command(BaseCommand):
    help = 'Load data from a YAML file into the database'

    def add_arguments(self, parser):
        parser.add_argument(type=str)

    def handle(self, *args, **options):
        try:
            with open('shop1.yaml', 'r') as file:
                data = yaml.safe_load(file)
            # for shop in data['shop']:
            #     Shop.objects.get_or_create(name=shop['name'], url=shop['url'])
            for category in data['categories']:
                Category.objects.get_or_create(id=category['id'], name=category['name'])
        except yaml.YAMLError as exc:
            print(exc)

