import requests
import time
from write_file import write_to_csv


COUNT = 600


def _get_url(offset, region):
    return f'https://api.detmir.ru/v2/products?filter=categories[].alias:lego;' \
           f'promo:false;withregion:{region}&expand=meta.facet.ages.adults,' \
           f'meta.facet.gender.adults,webp&meta=*&limit=30&' \
           f'offset={offset}&sort=popularity:desc'


def _get_headers():
    with open('headers.txt', 'r') as headers_file:
        data = headers_file.readlines()
        headers_dict = {}
        for line in data:
            line_lst = line.rstrip().split(': ')
            if line_lst[0][0] == ':':
                continue
            headers_dict |= {line_lst[0]: line_lst[1]}
        if not headers_dict:
            raise ValueError('not valid headers')
        return headers_dict


def _check_region_and_file_name(file_name, region):
    if region not in ['RU-SPE', 'RU-MOW']:
        raise ValueError('invalid region')
    if not file_name:
        raise ValueError('empty file_name')


def write_file(file_name: str, region: str):
    headers = _get_headers()
    offset = 0
    while COUNT - offset > 0:
        url = _get_url(offset, region)
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not write_to_csv(file_name, data, region):
            break
        offset += 30
        print(f'write items to {file_name}')
        time.sleep(2)


if __name__ == '__main__':
    # copy new headers from browser Request Headers to headers.txt before start
    write_file('spb_lego.csv', 'RU-SPE')
    write_file('msk_lego.csv', 'RU-MOW')
