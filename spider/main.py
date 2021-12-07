import json
import asyncio
import os

import requests
from loguru import logger
import sys
import django
import json
import urllib.parse
import cfscrape

pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../nano_backend')))
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../nano_backend/apps')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'nano_backend.settings.prod'

os.environ['MYSQL_HOST'] = '42.193.50.174'
os.environ['MYSQL_PORT'] = '3306'
os.environ['MYSQL_USER'] = 'nano'
os.environ['MYSQL_PASSWORD'] = 'nano'
os.environ['MYSQL_DATABASE'] = 'nano'
os.environ['REDIS_HOST'] = '192.168.239.128'
os.environ['FASTDFS_TRACKER_HOST'] = '42.193.50.174'
os.environ['MEDIA_HOST'] = 'media.nano.nagico.cn'
os.environ['DEFAULT_AVATAR'] = 'group1/M00/00/00/CgAABGGqR96AQ4yeAAAMK5bwTxs776.jpg '

django.setup()

from animes.models import Anime
from places.models import Place
from photos.models import Photo

anime_data = {}
place_data = {}
bangumi_data = {}

def get_banmugi_info(title):
    logger.info(f'get_banmugi_info: {title}')
    url = f'https://api.bgm.tv/search/subject/{urllib.parse.quote(title)}?type=2&responseGroup=medium'
    scraper = cfscrape.create_scraper()

    response = scraper.get(url)
    data = json.loads(response.text)
    logger.info(f'fetch_bangumi_info: {title}')
    return data['list'][0]


def get_banmugi_info_by_id(id):
    logger.info(f'get_banmugi_info: {id}')
    url = f'https://api.bgm.tv/subject/{id}?responseGroup=small'
    scraper = cfscrape.create_scraper()

    response = scraper.get(url)
    data = json.loads(response.text)
    logger.info(f'fetch_bangumi_info: {id}')
    return data


def bangumi():
    for anime_info in anime_data:
        if 'movie' in anime_data[anime_info]['data']:
            data = anime_data[anime_info]['data']['movie']
            try:
                res = get_banmugi_info(data['cname'])
                if res['name_cn'] == data['cname']:
                    bangumi_data.update({anime_info: res})
                else:
                    logger.warning(f'{data["cname"]} not found in bgm.tv')
            except:
                logger.error(f'get_banmugi_info_failed: {data["cname"]}')

    with open("bangumi_data.json", "w", encoding='utf-8') as f:
        json.dump(bangumi_data, f, ensure_ascii=False, indent=4)
        logger.info(f'bangumi_data.json saved')



if __name__ == "__main__":
    with open("anime_data.json", "r", encoding='utf-8') as f:
        anime_data = json.load(f)

    with open("place_data.json", "r", encoding='utf-8') as f:
        place_data = json.load(f)

    with open("bangumi_data.json", "r", encoding='utf-8') as f:
        bangumi_data = json.load(f)

    pass
