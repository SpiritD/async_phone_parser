import asyncio
from typing import List

from aiohttp import ClientSession


async def fetch(session: ClientSession, url: str) -> str:
    """
    Получение текста страницы по url.

    :param session: сессия клиента aiohttp
    :param url: адрес страницы
    :return: текст html страницы
    """
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


async def fetch_all(session: ClientSession, urls: List[str]) -> List[str]:
    """
    Создание асинхронных задач для получения текста страниц.

    :param session: сессия клиента aiohttp
    :param urls: адреса страниц
    :return: список текстов страниц
    """
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch(session, url))
        tasks.append(task)
    return await asyncio.gather(*tasks)


async def get_html_from_urls(urls: List[str]) -> List[str]:
    """
    Получаем исходный код всех страниц.

    Получение с помощью клиента из aiohttp.

    :param urls: адреса страниц
    :return: список текстов страниц
    """
    async with ClientSession() as session:
        return await fetch_all(session, urls)
