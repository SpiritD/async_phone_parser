import asyncio
import re
from typing import (
    Dict,
    List,
)

import phonenumbers
from aiohttp import ClientSession
from phonenumbers import PhoneNumber

from repository import Repository


national_format_converter = re.compile(r'[ \-()]')


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


def change_phone_format(phone_number: PhoneNumber) -> str:
    """
    Меняет формат номеров на 8KKKNNNNNNN.

    :param phone_number: объект с номером телефона
    :return: номер телефона в формате 8KKKNNNNNNN
    """
    return national_format_converter.sub(
        repl='',
        string=phonenumbers.format_number(
            numobj=phone_number,
            num_format=phonenumbers.PhoneNumberFormat.NATIONAL,
        ),
    )


async def main(repository: Repository):
    """Основная функция для получения номеров телефонов с сайтов."""
    urls = repository.get_urls()
    # структура для хранения списка номеров для каждого сайта
    parsed_numbers: Dict[str, List[str]] = {}

    # получаем исходный код всех страниц
    async with ClientSession() as session:
        raw_html_list = await fetch_all(session, urls)

    # соответствие страницы сайта и его html
    for site, source_code in zip(urls, raw_html_list):
        parsed_numbers[site] = []
        # поиск всех номеров на странице
        for phone in phonenumbers.PhoneNumberMatcher(source_code, 'RU'):
            # добавляем к сайту, преобразуя формат
            parsed_numbers[site].append(
                change_phone_format(
                    phone_number=phone.number,
                ),
            )

    # сохраняем результаты
    repository.save_phone_numbers(parsed_numbers=parsed_numbers)


if __name__ == '__main__':
    asyncio.run(main(
        repository=Repository(),
    ))
