import aiohttp
import asyncio
from loguru import logger


class PlaceSpider:
    def __init__(self):
        self.session = aiohttp.ClientSession(loop=asyncio.get_event_loop())

    async def close(self):
        await self.session.close()

    async def get_place_info(self, place_id):
        logger.info(f"Start to get place info for {place_id}")
        url = f'https://mocation.fotoplace.cc/api/place/{place_id}'
        async with self.session.get(url) as response:
            data = await response.json()
            logger.success(f"Get place info for {place_id}")
            if data['data']['place'] is None:
                return None
            return {place_id: data}
