import factory
from factory import errors
from factory.alchemy import (
    SESSION_PERSISTENCE_COMMIT,
    SESSION_PERSISTENCE_FLUSH,
)
from factory.builder import StepBuilder, BuildStep, parse_declarations
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from src.api.models import OFDItem, OFDReceipt
import inspect

from tests.mocks.faker_providers.ofd import OfdProvider

factory.Faker._DEFAULT_LOCALE = "ru_RU"
factory.Faker.add_provider(OfdProvider)


class AsyncFactory(factory.alchemy.SQLAlchemyModelFactory):
    @classmethod
    async def _generate(cls, strategy, params):
        if cls._meta.abstract:
            raise factory.errors.FactoryError(
                "Cannot generate instances of abstract factory %(f)s; "
                "Ensure %(f)s.Meta.model is set and %(f)s.Meta.abstract "
                "is either not set or False." % {"f": cls.__name__}
            )

        step = AsyncStepBuilder(cls._meta, params, strategy)
        return await step.build()

    @classmethod
    async def _get_or_create(cls, model_class, session, args, kwargs):
        key_fields = {}
        for field in cls._meta.sqlalchemy_get_or_create:
            if field not in kwargs:
                raise errors.FactoryError(
                    "sqlalchemy_get_or_create - "
                    "Unable to find initialization value for '%s' in factory %s"
                    % (field, cls.__name__)
                )
            key_fields[field] = kwargs.pop(field)

        obj = (
            await session.execute(
                select(model_class).filter_by(*args, **key_fields)
            )
        ).scalar_one_or_none()

        if not obj:
            try:
                obj = await cls._save(
                    model_class, session, args, {**key_fields, **kwargs}
                )
            except IntegrityError as e:
                await session.rollback()

                if cls._original_params is None:
                    raise e

                get_or_create_params = {
                    lookup: value
                    for lookup, value in cls._original_params.items()
                    if lookup in cls._meta.sqlalchemy_get_or_create
                }
                if get_or_create_params:
                    try:
                        obj = (
                            await session.execute(
                                select(model_class).filter_by(
                                    **get_or_create_params
                                )
                            )
                        ).scalar_one()
                    except NoResultFound:
                        raise e from None
                else:
                    raise e

        return obj

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        for key, value in kwargs.items():
            if inspect.isawaitable(value):
                kwargs[key] = await value
        return await super()._create(model_class, *args, **kwargs)

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]

    @classmethod
    async def _save(cls, model_class, session, args, kwargs):
        session_persistence = cls._meta.sqlalchemy_session_persistence
        obj = model_class(*args, **kwargs)
        session.add(obj)
        if session_persistence == SESSION_PERSISTENCE_FLUSH:
            await session.flush()
        elif session_persistence == SESSION_PERSISTENCE_COMMIT:
            await session.commit()
        return obj


class AsyncStepBuilder(StepBuilder):
    async def build(self, parent_step=None, force_sequence=None):
        """Build a factory instance."""
        # TODO: Handle "batch build" natively
        pre, post = parse_declarations(
            self.extras,
            base_pre=self.factory_meta.pre_declarations,
            base_post=self.factory_meta.post_declarations,
        )

        if force_sequence is not None:
            sequence = force_sequence
        elif self.force_init_sequence is not None:
            sequence = self.force_init_sequence
        else:
            sequence = self.factory_meta.next_sequence()

        step = BuildStep(
            builder=self,
            sequence=sequence,
            parent_step=parent_step,
        )
        step.resolve(pre)

        args, kwargs = self.factory_meta.prepare_arguments(step.attributes)

        instance = await self.factory_meta.instantiate(
            step=step,
            args=args,
            kwargs=kwargs,
        )

        postgen_results = {}
        for declaration_name in post.sorted():
            declaration = post[declaration_name]
            declaration_result = declaration.declaration.evaluate_post(
                instance=instance,
                step=step,
                overrides=declaration.context,
            )
            if inspect.isawaitable(declaration_result):
                declaration_result = await declaration_result
            postgen_results[declaration_name] = declaration_result

        self.factory_meta.use_postgeneration_results(
            instance=instance,
            step=step,
            results=postgen_results,
        )
        return instance


class OFDReceiptFactory(AsyncFactory):
    class Meta:
        model = OFDReceipt
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_COMMIT

    qrraw = factory.Faker("ofd_qr")
    user = factory.Faker("company")
    user_inn = factory.Faker("businesses_inn")
    seller_address = factory.Faker("company_email")
    retail_place = factory.Faker("uri")
    retail_place_address = factory.Faker("address")
    region = factory.Faker("numerify", text="!#")
    date_time = factory.Faker("date_time_between")
    credit_sum = factory.Faker(
        "pyfloat", right_digits=2, min_value=0, max_value=10000
    )
    code = factory.Faker("random_int", min=1, max=9)
    operation_type = 1
    total_sum = factory.Faker(
        "pyfloat", right_digits=2, min_value=0, max_value=10000
    )
    buyer_phone_or_address = factory.Faker("phone_number")


class OFDItemFactory(AsyncFactory):
    class Meta:
        model = OFDItem
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_COMMIT

    # id: Mapped[int]
    name = factory.Faker("ofd_item_name")
    price = factory.Faker(
        "pyfloat", right_digits=2, min_value=0, max_value=3000
    )
    quantity = factory.Faker("random_int", min=1, max=9)
    items_quantity_measure = 0

    receipt = factory.SubFactory(OFDReceiptFactory)
