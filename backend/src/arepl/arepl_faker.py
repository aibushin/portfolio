from arepl_dump import dump  # type: ignore  # noqa: F401
from faker import Faker

fake = Faker(locale="ru_RU")

qwe = fake.company()
asd = fake.numerify(text="!#")
