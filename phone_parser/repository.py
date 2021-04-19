from typing import (
    Dict,
    List,
)


class Repository:
    """Класс для работы с хранилищем."""

    def get_urls(self) -> List[str]:
        """
        Получение url адресов для парсинга номеров.

        Здесь может быть получение адресов из базы или другого источника.

        :return: список страниц сайтов
        """
        return [
            'https://masterdel.ru',
            'https://repetitors.info',
        ]

    def save_phone_numbers(self, parsed_numbers: Dict[str, List[str]]) -> None:
        """
        Сохраняет полученные номера телефонов.

        Здесь может быть сохранение в базу, отправка по апи или просто вывод в консоль как сейчас.

        :param parsed_numbers: список номеров по сайтам
        """
        print(parsed_numbers)
