from datetime import datetime
from io import BytesIO
from faker.providers import BaseProvider
from faker import Faker
import pyqrcode

fake = Faker("ru_RU")


class OfdProvider(BaseProvider):
    item_name = [
        "1 X Полисомнографическое исследование ночное",
        "NATROL Fall sleep faster,быстрорастворимый, с клубничным вкусом 5 мг, 90 таблеток из США, доставка почтой",  # noqa: E501
        "Ананасы кусочки Botanica в сиропе",
        "Витамин Д3 5000 Natrol, для взрослых натрол Vitamin D3 5000 ME Natrol для иммунитета, метаболизма, иммуномодулятор 90 таб",  # noqa: E501
        "Витамины, бад, для нервной системы, от стресса, Натрол, 5HTP, Natrol 5-HTP, 5 HTP 50mg 45 капс",  # noqa: E501
        "Вода Святой источник без газа",
        'Кинза зелень сушеная (кориандра лист сушеный), "Индана" 75 гр./500 мл.',  # noqa: E501
        "КЛЮК В С.ПУД 120Г",
        "Масло подсолнечное Слобода",
        "Нектар Апельсин-манго Rich",
        "Оплата по номеру: 6672463",
        "Пакет-майка 'ВкусВилл' малый",
        "ПЕЛЬМ ГОСУД ИМПЕР",
        "Персики половинки Botanica в сиропе",
        "Пододеяльник ночь хлопок 200*220",
        "Салат из огурцов Знаток",
        "Сахар-песок Русский",
        "СТЕЙК РИБАЙ ГОВЯЖ320",
        "Томаты протёртые Napolina",
        "Торт 'Маракуйя'",
        "Торт 'Сметанный' с малиной",
        "Торт медово-сметанный Из Лавки со сгущёнкой",
        "Торт Наполеон Из Лавки Домашний",
        "Тяжёлое одеяло льняное 200*220 18 кг",
        "Уксус столовый Uni Dan",
        "Уксус яблочный K?hne",
        "Упаковка заказа",
        "Услуги доставки",
        "Фарш говяжий Black Angus Мираторг",
        "Хурма 'ВВ отборное', 2 шт",
        "Хурма Бычье сердце, 2 шт",
        "ХУРМА СВЕЧА ВЕС",
        "ХУРМА ШАРОН ВЕС",
        "Чаевые",
        "Чай травяной Greenfield двойная мята",
        "Чай чёрный Kenyan Sunrise Greenfield",
        "Чай чёрный Spring Melody Greenfield",
        "ЯЙЦО СТОЛОВОЕ СО 10",
    ]

    def ofd_qr(self) -> str:
        """Данные QR-кода в формате ОФД."""
        date = datetime.now().strftime("%Y%m%d")
        time = fake.time(pattern="%H%M")
        price = fake.pydecimal(min_value=100, max_value=10000, right_digits=2)
        fn = self.random_number(digits=16, fix_len=True)
        fd = self.random_number(digits=6, fix_len=True)
        fp = self.random_number(digits=9, fix_len=True)

        return f"t={date}T{time}&s={price}&fn={fn}&i={fd}&fp={fp}&n=1"

    def ofd_item_name(self):
        return self.random_element(self.item_name)

    def ofd_qr_image(self, content=None, mode="binary") -> bytes:
        if not content:
            content = self.ofd_qr()
        qr = pyqrcode.create(content=content, mode=mode)
        io = BytesIO()
        qr.png(io, scale=2)
        return io


fake.add_provider(OfdProvider)
