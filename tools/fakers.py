"""Генераторы фейковых данных для нагрузочного тестирования.

Модуль предоставляет класс Fake — обёртку над Faker для генерации
тестовых данных в русскоязычном и англоязычном форматах.

Поддерживаемые типы данных:
- Email, имена, телефоны
- Перечисления (enum) для proto-контрактов
- Финансовые суммы и категории операций
"""

from uuid import uuid4
from faker import Faker
from faker.providers.python import TEnum
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper

class Fake:
    """Обёртка над Faker для генерации тестовых данных.

    Предоставляет методы для генерации специализированных данных,
    используемых в performance-тестах финансовой системы.

    Attributes:
        faker: Экземпляр Faker для генерации базовых данных.

    Example:
        >>> faker_ru = Fake(faker=Faker('ru_RU'))
        >>> email = faker_ru.email()
        >>> amount = faker_ru.amount()
    """

    def __init__(self, faker: Faker):
        """Инициализировать генератор фейковых данных.

        Args:
            faker: Экземпляр Faker с нужной локалью.
        """
        self.faker = faker

    def enum(self, value: type[TEnum]):
        """Сгенерировать случайное значение enum.

        Args:
            value: Тип перечисления.

        Returns:
            Случайное значение из перечисления.
        """
        return self.faker.enum(value)

    def proto_enum(self, value: EnumTypeWrapper) -> int:
        """Сгенерировать случайное значение proto-enum.

        Args:
            value: Обёртка перечисления protobuf.

        Returns:
            Случайное целое значение из перечисления.
        """
        return self.faker.random_element(value.values())

    def email(self):
        """Сгенерировать уникальный email адрес.

        Returns:
            Email адрес с UUID-префиксом.
        """
        return f'{str(uuid4())[:6]}.{self.faker.email()}'

    def category(self):
        """Сгенерировать случайную категорию операции.

        Returns:
            Название категории (gas, taxi, tolls, и т.д.).
        """
        cat = [
            "gas",
            "taxi",
            "tolls",
            "water",
            "beauty",
            "mobile",
            "travel",
            "parking",
            "catalog",
            "internet",
            "satellite",
            "education",
            "government",
            "healthcare",
            "restaurants",
            "electricity",
            "supermarkets",
        ]
        return self.faker.random_element(cat)

    def last_name(self):
        """Сгенерировать фамилию.

        Returns:
            Случайная фамилия.
        """
        return self.faker.last_name()

    def first_name(self):
        """Сгенерировать имя.

        Returns:
            Случайное имя.
        """
        return self.faker.first_name()

    def middle_name(self):
        """Сгенерировать отчество.

        Returns:
            Случайное отчество.
        """
        return self.faker.first_name()

    def phone_number(self):
        """Сгенерировать номер телефона.

        Returns:
            Случайный номер телефона.
        """
        return self.faker.phone_number()

    def float(self, start: int = 1, end: int = 100):
        """Сгенерировать случайное дробное число.

        Args:
            start: Минимальное значение (по умолчанию 1).
            end: Максимальное значение (по умолчанию 100).

        Returns:
            Случайное число с 2 знаками после запятой.
        """
        return self.faker.pyfloat(min_value=start, max_value=end, right_digits=2)

    def amount(self):
        """Сгенерировать случайную денежную сумму.

        Returns:
            Сумма от 1 до 1000 с 2 знаками после запятой.
        """
        return self.float(1, 1000)

faker_ru = Fake(faker=Faker('ru_RU'))
faker_en = Fake(faker=Faker('en_US'))
