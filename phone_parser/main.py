import asyncio
import re
from typing import (
    Dict,
    List,
)

import phonenumbers
from phonenumbers import PhoneNumber

from client import get_html_from_urls
from repository import Repository


national_format_converter = re.compile(r'[ \-()]')


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
    raw_html_list = await get_html_from_urls(urls=urls)

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
