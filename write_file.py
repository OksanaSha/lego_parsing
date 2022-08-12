import json
import csv
import os


FIELDNAMES = ['id', 'title', 'price', 'promo_price', 'url']

def _get_price(item_data: dict) -> dict:
    if item_data['promo']:
        prices = {
            'price': item_data['old_price']['price'],
            'promo_price': item_data['price']['price']
        }
    else:
        prices = {
            'price': item_data['price']['price'],
            'promo_price': None
        }
    return prices


def _check_city(item_data: dict, region: str) -> bool:
    return region in item_data['available']['offline']['region_iso_codes']


def prepare_data(data: dict, region: str) -> dict:
    if data:
        for item in data['items']:
            if not _check_city(item, region):
                break
            prepare_item_data = {
                'id': item['id'],
                'title': item['title'],
                'url': item['link']['web_url']
            }
            prepare_item_data |= _get_price(item)
            yield prepare_item_data


def _create_csv(file_name):
    with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
        writer.writeheader()


def write_to_csv(file_name: str, data: dict, region: str):
    if not os.path.exists(file_name):
        _create_csv(file_name)
    items_data = [item for item in prepare_data(data, region)]
    if items_data:
        with open(file_name, 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES, delimiter=',')
            writer.writerows(items_data)
        return True


# with open('lego_spb.csv', 'w') as csv_file:
#     fieldnames = ['id', 'title', 'price', 'promo_price', 'url']
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',')
#     writer.writeheader()
#     writer.writerows([item for item in prepare_data(data, region='RU-SPE')])
