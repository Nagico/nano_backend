
async def main_spider():
    # id_list = [3857, 1741, 4998, 4472]
    id_list = list(range(0, 99999))
    tasks = []
    spider = MovieSpider()
    for item in id_list:
        tasks.append(asyncio.create_task(spider.get_movie_info(item)))

    done, pendding = await asyncio.wait(tasks)

    await spider.close()

    for item in done:
        result = item.result()
        if result is not None:
            data.update(result)


def spider_movie():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_spider())
    with open("data.json", "w") as f:
        json.dump(data, f)


def down_cover(title: str, cover_url: str) -> str:
    """
    下载封面

    :param title: 电影名称

    :param cover_url: 封面 url

    :return: 封面文件的路径
    """
    ext_name = cover_url.split('.')[-1]  # 获取 url 中文件的扩展名
    cover_name = f'cover/{title}.{ext_name}'  # 封面保存路径
    logger.debug(f'Download cover: {cover_name}')

    response = requests.get(cover_url)  # 下载封面图片
    img = response.content
    with open(f'{cover_name}', 'wb+') as f:  # 写入文件
        f.write(img)
    return cover_name


place_list = []


async def main_spider_place():
    tasks = []
    spider = PlaceSpider()
    for item in place_list:
        tasks.append(asyncio.create_task(spider.get_place_info(item)))

    done, pendding = await asyncio.wait(tasks)

    await spider.close()

    for item in done:
        result = item.result()
        if result is not None:
            data.update(result)


def spider_place():
    with open("anime_data.json", "r") as f:
        data = json.load(f)

    for key, value in data.items():
        place_list += value['data']['movie']['placeIds']

    place_list = list(set(place_list))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_spider_place())
    with open("place_data.json", "w") as f:
        json.dump(data, f)