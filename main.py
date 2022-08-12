import requests
import time
from write_to_file import write_to_csv


COUNT = 600
HEADERS = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'if-none-match': 'W/"54ac4-J9RG/aGVmI2nff2uYuniniZlJgg"',
    'origin': 'https://www.detmir.ru',
    'referer': 'https://www.detmir.ru/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/104.0.0.0 Safari/537.36',
    'x-requested-with': 'detmir-ui'
}


def _get_url(offset: int, region):
    return f'https://api.detmir.ru/v2/products?filter=categories[].alias:' \
           f'lego;promo:false;withregion:{region}&expand=meta.facet.ages.' \
           f'adults,meta.facet.gender.adults,webp&meta=*&limit=30&' \
           f'offset={offset}&sort=popularity:desc'


def _check_region_and_file_name(file_name: str, region: str):
    if region not in ['RU-SPE', 'RU-MOW']:
        raise ValueError('invalid region')
    if not file_name:
        raise ValueError('empty file_name')


def write_file(file_name: str, region: str):
    offset = 0
    while COUNT - offset > 0:
        url = _get_url(offset, region)
        response = requests.get(url=url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if not write_to_csv(file_name, data, region):
            break
        offset += 30
        print(f'write items to {file_name}')
        time.sleep(2) #sleep not to get banned as bot


if __name__ == '__main__':
    write_file('spb_lego.csv', 'RU-SPE')
    write_file('msk_lego.csv', 'RU-MOW')
