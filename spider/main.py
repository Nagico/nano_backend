import json
import asyncio
import os

import requests
import re

from zhon.hanzi import punctuation
from loguru import logger
import sys
import django
import json
import urllib.parse
import cfscrape

from nano_backend.utils.choices import ImageTypeChoice
logger.add("runtime.log")

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
os.environ['DEFAULT_AVATAR'] = 'group1/M00/00/00/CgAABGGqR96AQ4yeAAAMK5bwTxs776.jpg'

django.setup()

from animes.models import Anime
from places.models import Place
from photos.models import Photo
from users.models import User
from fdfs_client.client import Fdfs_client, get_tracker_conf

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


def down_pic(url):
    logger.info(f'down_pic: {url}')
    scraper = cfscrape.create_scraper()
    response = scraper.get(url)
    res = response.content
    return res


if __name__ == "__main__":

    tracker_conf = get_tracker_conf('../nano_backend/utils/fastdfs/client.conf')
    tracker_conf['host_tuple'] = (os.environ.get('FASTDFS_TRACKER_HOST', tracker_conf['host_tuple'][0]),)
    client = Fdfs_client(tracker_conf)

    user = User.objects.get(id=1)

    with open("anime_data.json", "r", encoding='utf-8') as f:
        anime_data = json.load(f)

    with open("place_data.json", "r", encoding='utf-8') as f:
        place_data = json.load(f)

    with open("bangumi_data.json", "r", encoding='utf-8') as f:
        bangumi_data = json.load(f)

    bangumi_data['4849'] = get_banmugi_info_by_id(891)
    # client.delete_file(str.encode('group1/M00/00/00/CgAABGGwNniAP95UAACmUZUO3nA227.jpg'))
    # client.delete_file(str.encode('group1/M00/00/00/CgAABGGwNnmAUgOhAAAE5VdrGvg332.jpg'))

    # with open('file', 'r', encoding='utf-8') as f:
    #     file_lines = f.readlines()
    #     for line in file_lines:
    #         if 'group1/' in line:
    #             url = line.strip('\n').split(' ')[-1]
    #             try:
    #                 client.delete_file(str.encode(url))
    #                 logger.info(f'delete_file: {url}')
    #             except:
    #                 logger.debug('skip')

    flag = False
    for anime_id in anime_data:
        if anime_id == '4903':
            flag = True
        if not flag:
            continue

        cover_url = bangumi_data[anime_id]['images']['large']
        cover_small_url = bangumi_data[anime_id]['images']['grid']
        cover_fdsf = client.upload_by_buffer(down_pic(cover_url), file_ext_name=cover_url.rsplit('.', 1)[1])
        logger.warning(cover_fdsf['Remote file_id'].decode())
        cover_small_fdfs = client.upload_by_buffer(down_pic(cover_small_url),
                                                   file_ext_name=cover_small_url.rsplit('.', 1)[1])
        logger.warning(cover_small_fdfs['Remote file_id'].decode())
        anime = Anime(
            title=bangumi_data[anime_id]['name'],
            title_cn=bangumi_data[anime_id]['name_cn'],
            description=bangumi_data[anime_id]['summary'],
            cover=cover_fdsf['Remote file_id'].decode(),
            cover_small=cover_small_fdfs['Remote file_id'].decode(),
            create_user=user,
            collection_num=0,
            is_public=True,
            is_approved=True,
        )
        anime.save()
        anime.contributor.add(user)
        anime.save()

        logger.success(f'create anime: {anime.title}')
        # clean
        # client.delete_file(cover_fdsf['Remote file_id'])
        # client.delete_file(cover_small_fdfs['Remote file_id'])

        for plot in anime_data[anime_id]['data']['movie']['plots']:
            place_info = place_data[str(plot['placeId'])]['data']['place']
            if place_info['level1Cname'] != '日本':
                logger.debug(f'skip place: {place_info["cname"]}')
                continue
            place = Place(
                name=plot['placeCname'],
                address=place_info['caddress'],
                city=place_info['areaCname'],
                latitude=place_info['lat'],
                longitude=place_info['lng'],
                description=place_info['description'],
                anime_id=anime,
                create_user=user,
                collection_num=0,
                is_public=True,
                is_approved=True,
            )
            place.save()
            place.contributor.add(user)
            place.save()

            logger.success(f'create place: {place.name}')

            r_cnt = 0
            for real_pic in place_info['realGraphics']:
                real_pic_url = real_pic['picPath']
                if real_pic_url == '':
                    continue
                real_pic_fdsf = client.upload_by_buffer(down_pic(real_pic_url),
                                                        file_ext_name=real_pic_url.rsplit('.', 1)[1])
                logger.warning(real_pic_fdsf['Remote file_id'].decode())
                r_cnt += 1
                real_pic = Photo(
                    name=f'{place.name}_{r_cnt}',
                    description=real_pic['description'],
                    image=real_pic_fdsf['Remote file_id'].decode(),
                    type=ImageTypeChoice.REAL,
                    anime_id=anime,
                    place_id=place,
                    create_user=user,
                    is_public=True,
                    is_approved=True,
                )
                real_pic.save()
                logger.success(f'[{anime.title_cn}] create real_pic: {real_pic.name}')

                # clean
                # client.delete_file(real_pic_fdsf['Remote file_id'])

            for item in place_info['scenes']:
                if anime_id == str(item['movieId']):
                    for detail in item['details']:
                        cnt = 0
                        c_cnt = 0
                        pic_name = f'{place.name}-{anime.title_cn}'
                        pic_des = detail['description']

                        for pic in detail['stills']:
                            pic_url = pic['picPath']
                            if pic_url == '':
                                continue
                            pic_fdsf = client.upload_by_buffer(down_pic(pic_url),
                                                               file_ext_name=pic_url.rsplit('.', 1)[1])
                            logger.warning(pic_fdsf['Remote file_id'].decode())
                            if pic_url.rsplit('.', 1)[1].lower() == 'gif':
                                c_cnt += 1
                                photo = Photo(
                                    name=f'{pic_name} 对比{c_cnt}',
                                    description=pic_des,
                                    image=pic_fdsf['Remote file_id'].decode(),
                                    type=ImageTypeChoice.OTHER,
                                    anime_id=anime,
                                    place_id=place,
                                    create_user=user,
                                    is_public=True,
                                    is_approved=True,
                                )
                            else:
                                cnt += 1
                                photo = Photo(
                                    name=f'{pic_name} 剧照{cnt}',
                                    description=pic_des,
                                    image=pic_fdsf['Remote file_id'].decode(),
                                    type=ImageTypeChoice.VIRTUAL,
                                    anime_id=anime,
                                    place_id=place,
                                    create_user=user,
                                    is_public=True,
                                    is_approved=True,
                                )
                            photo.save()
                            logger.success(f'[{anime.title_cn}] create virtual photo: {photo.name}')
                            # clean
                            # client.delete_file(pic_fdsf['Remote file_id'])
    pass
