from uuid import uuid4
from faker import Faker
from faker.providers.python import TEnum

class Fake:
    def __init__(self, faker: Faker):
        self.faker = faker


    def enum(self, value: type[TEnum]):
        return self.faker.enum(value)

    def email(self):
        return f'{str(uuid4())[:6]}.{self.faker.email()}'

    def category(self):
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
        return self.faker.last_name()

    def first_name(self):
        return self.faker.first_name()

    def middle_name(self):
        return self.faker.first_name()

    def phone_number(self):
        return self.faker.phone_number()

    def float(self, start: int = 1, end: int = 100):
        return self.faker.pyfloat(min_value=start, max_value=end, right_digits=2)

    def amount(self):
        return self.float(1, 1000)

faker_ru = Fake(faker=Faker('ru_RU'))
faker_en = Fake(faker=Faker('en_US'))
