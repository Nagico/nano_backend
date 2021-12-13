import json
import asyncio
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import re

from zhon.hanzi import punctuation
from bs4 import BeautifulSoup
from loguru import logger
import sys
import datetime
import django
import json
import urllib.parse
import cfscrape

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
os.environ['REDIS_HOST'] = '127.0.0.1'
os.environ['FASTDFS_TRACKER_HOST'] = '42.193.50.174'
os.environ['MEDIA_HOST'] = 'media.nano.nagico.cn'
os.environ['DEFAULT_AVATAR'] = ''

django.setup()

from animes.models import Anime, AnimeAlias
from places.models import Place
from photos.models import Photo
from users.models import User
from fdfs_client.client import Fdfs_client, get_tracker_conf
from nano_backend.utils.choices import ImageTypeChoice
from staffs.models import Staff
from tags.models import Tag

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

def get_extra_info_by_bangumi_id(id):
    logger.info(f'get_extra_info_by_bangumi_id: {id}')
    url = f'https://cdn.jsdelivr.net/gh/czy0729/Bangumi-Subject@master/data/{id//100}/{id}.json'
    scraper = cfscrape.create_scraper()

    response = scraper.get(url)
    data = json.loads(response.text)
    logger.info(f'fetch_extra_info: {id}')
    return data

def down_pic(url):
    logger.info(f'down_pic: {url}')
    scraper = cfscrape.create_scraper()
    response = scraper.get(url)
    res = response.content
    return res


def create_first():
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


def add_by_bangumi_id(id):
    tracker_conf = get_tracker_conf('../nano_backend/utils/fastdfs/client.conf')
    tracker_conf['host_tuple'] = (os.environ.get('FASTDFS_TRACKER_HOST', tracker_conf['host_tuple'][0]),)
    client = Fdfs_client(tracker_conf)

    user = User.objects.get(id=1)
    data = get_banmugi_info_by_id(id)
    if Anime.objects.filter(title=data['name']).count() != 0:
        logger.warning(f'[{data["name_cn"]}] already exists')
        return
    cover_url = data['images']['large']
    cover_small_url = data['images']['grid']
    cover_medium_url = data['images']['common']
    cover_fdsf = client.upload_by_buffer(down_pic(cover_url), file_ext_name=cover_url.rsplit('.', 1)[1])
    logger.warning(cover_fdsf['Remote file_id'].decode())
    cover_small_fdfs = client.upload_by_buffer(down_pic(cover_small_url),
                                               file_ext_name=cover_small_url.rsplit('.', 1)[1])
    logger.warning(cover_small_fdfs['Remote file_id'].decode())
    cover_medium_fdsf = client.upload_by_buffer(down_pic(cover_medium_url),
                                                file_ext_name=cover_medium_url.rsplit('.', 1)[1])
    logger.warning(cover_medium_fdsf['Remote file_id'].decode())
    anime = Anime(
        title=data['name'],
        title_cn=data['name_cn'] if data['name_cn'] != '' else data['name'],
        description=data['summary'],
        cover=cover_fdsf['Remote file_id'].decode(),
        cover_medium=cover_medium_fdsf['Remote file_id'].decode(),
        cover_small=cover_small_fdfs['Remote file_id'].decode(),
        create_user=user,
        collection_num=0,
        is_public=True,
        is_approved=True,
    )
    anime.save()
    anime.contributor.add(user)
    anime.save()
    logger.info(f'add extra info: {id}')
    # anime = Anime.objects.get(title_cn=anime_info['name_cn'])
    extra_info = get_extra_info_by_bangumi_id(id)
    info = extra_info['info']
    soup = BeautifulSoup(info)

    try:
        air_date = datetime.datetime.strptime(soup.find_all(text=re.compile(r"\d{4}年\d{1,2}月\d{1,2}日"))[0].text,
                                              "%Y年%m月%d日")
        anime.air_date = air_date
        logger.debug(f'{anime.id} air_date: {air_date}')
    except:
        pass

    tags = []
    for tag in [_['name'] for _ in extra_info['tags']]:
        tags.append(Tag.objects.get_or_create(name=tag)[0])
    anime.tags.set(tags)
    logger.debug(f'{anime.id} tags: {tags}')

    try:
        epi_num = int(soup.find_all(text='话数: ')[0].next.text)
        anime.epi_num = epi_num
        logger.debug(f'{anime.id} epi_num: {epi_num}')
    except:
        pass

    try:
        director = soup.find_all(text='导演: ')[0].next.text
        anime.director.set([Staff.objects.get_or_create(name=director)[0]])
        logger.debug(f'{anime.id} director: {director}')
    except:
        pass

    try:
        original = soup.find_all(text='原作: ')[0].next.text
        anime.original.set([Staff.objects.get_or_create(name=original)[0]])
        logger.debug(f'{anime.id} original: {original}')
    except:
        pass

    try:
        script = soup.find_all(text='脚本: ')[0].parent.parent.text.replace('脚本: ', '').split('、')
        items = []
        for item in script:
            items.append(Staff.objects.get_or_create(name=item)[0])
        anime.script.set(items)
        logger.debug(f'{anime.id} script: {script}')
    except:
        pass

    try:
        storyboard = soup.find_all(text='分镜: ')[0].parent.parent.text.replace('分镜: ', '').split('、')
        items = []
        for item in storyboard:
            items.append(Staff.objects.get_or_create(name=item)[0])
        anime.storyboard.set(items)
        logger.debug(f'{anime.id} storyboard: {storyboard}')
    except:
        pass

    try:
        actor = soup.find_all(text='演出: ')[0].parent.parent.text.replace('演出: ', '').split('、')
        items = []
        for item in actor:
            items.append(Staff.objects.get_or_create(name=item)[0])
        anime.actor.set(items)
        logger.debug(f'{anime.id} actor: {actor}')
    except:
        pass

    try:
        music = soup.find_all(text='音乐: ')[0].next.text
        anime.music.set([Staff.objects.get_or_create(name=music)[0]])
        logger.debug(f'{anime.id} music: {music}')
    except:
        pass

    try:
        producer = soup.find_all(text='动画制作: ')[0].next.text
        anime.producer.set([Staff.objects.get_or_create(name=producer)[0]])
        logger.debug(f'{anime.id} producer: {producer}')
    except:
        pass

    try:
        website = soup.find_all(text='官方网站: ')[0].next.text
        anime.website = website
        logger.debug(f'{anime.id} website: {website}')
    except:
        pass

    anime.country = '日本'

    try:
        alias = []
        node = soup.find_all(text='别名: ')[0].parent.parent
        while '别名' in node.text:
            alias.append(node.text.replace('别名: ', ''))
            node = node.next_sibling
        for item in alias:
            AnimeAlias.objects.create(title=item, anime=anime)
            logger.debug(f'{anime.id} alias: {item}')
    except:
        pass

    # clean
    # client.delete_file(cover_medium_fdsf['Remote file_id'])
    # client.delete_file(cover_fdsf['Remote file_id'])
    # client.delete_file(cover_small_fdfs['Remote file_id'])
    anime.save()
    logger.success(f'create anime: {anime.title}')
    return f'create anime: {anime.title}'

if __name__ == "__main__":
    with open("anime_data.json", "r", encoding='utf-8') as f:
        anime_data = json.load(f)

    with open("place_data.json", "r", encoding='utf-8') as f:
        place_data = json.load(f)

    with open("bangumi_data.json", "r", encoding='utf-8') as f:
        bangumi_data = json.load(f)

    # bangumi_data['4849'] = get_banmugi_info_by_id(891)
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
    url = 'https://bgm.tv/anime/tag/%E9%9D%92%E6%98%A5?page='
    # url = 'https://bgm.tv/anime/tag/%E4%BA%AC%E9%98%BF%E5%B0%BC?page='
    # for i in range(8, 20):
    #     with open('id.json', 'r', encoding='utf-8') as f:
    #         id_list = json.load(f)
    #     url_i = url + str(i)
    #     logger.info(f'url: {url_i}')
    #     scraper = cfscrape.create_scraper()
    #     response = scraper.get(url_i)
    #     data = response.text
    #     soup = BeautifulSoup(data, 'html.parser')
    #     l = [eval(_['id'].replace('item_', '')) for _ in soup.find_all('li', class_='item odd clearit')]
    #     id_list = id_list + l
    #     id_list = list(set(id_list))
    #     logger.info(f'len: {len(id_list)}')
    #     with open('id.json', 'w', encoding='utf-8') as f:
    #         json.dump(id_list, f)
    with open('id.json', 'r', encoding='utf-8') as f:
        id_list = json.load(f)

    with ThreadPoolExecutor(max_workers=20) as t:
        obj_list = []
        for item in id_list:
            obj = t.submit(add_by_bangumi_id, item)
            obj_list.append(obj)

        for future in as_completed(obj_list):
            data = future.result()
            print(f"main: {data}")

