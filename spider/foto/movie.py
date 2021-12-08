import aiohttp
import asyncio
from loguru import logger


class MovieSpider:
    def __init__(self):
        self.session = aiohttp.ClientSession(loop=asyncio.get_event_loop())

    async def close(self):
        await self.session.close()

    async def get_movie_info(self, movie_id):
        logger.info(f"Start to get movie info for {movie_id}")
        url = f'https://mocation.fotoplace.cc/api/movie/{movie_id}'
        async with self.session.get(url) as response:
            data = await response.json()
            logger.success(f"Get movie info for {movie_id}")
            if data['data']['movie'] is None:
                return None
            return {movie_id: data}
