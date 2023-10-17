from pprint import pprint
import yaml
import json
data_dict = {}
lst = []
with open('fixtures/shop1.yaml', 'r', encoding='utf8') as file:
    data = yaml.safe_load(file)
pprint(data)

# with open ('data.json', 'w', encoding='utf-8') as json_file:
#     json.dump(lst, json_file, indent=2)
# for item in serializers.deserialize('json', serialized_data):
#     print(item)

# for category in data['categories']:
#     print(category['id'])
