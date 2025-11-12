from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class OFDItem(Base):
    __tablename__ = "ofd_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    price: Mapped[int] = mapped_column(BigInteger)
    quantity: Mapped[float]
    items_quantity_measure: Mapped[int | None]

    receipt_id: Mapped[str] = mapped_column(
        ForeignKey("ofd_receipts.qrraw", name="ofd_items_receipt_id_fkey", ondelete="CASCADE")
    )
    receipt: Mapped["OFDReceipt"] = relationship(back_populates="items", passive_deletes=True)


class OFDReceipt(Base):
    __tablename__ = "ofd_receipts"

    qrraw: Mapped[str] = mapped_column(primary_key=True)

    user: Mapped[str]
    user_inn: Mapped[str]
    seller_address: Mapped[str | None]
    retail_place: Mapped[str]
    retail_place_address: Mapped[str | None]

    region: Mapped[str]
    date_time: Mapped[datetime]
    credit_sum: Mapped[int]
    code: Mapped[int]
    operation_type: Mapped[int]
    total_sum: Mapped[int] = mapped_column(BigInteger)

    buyer_phone_or_address: Mapped[str | None]

    items: Mapped[list["OFDItem"]] = relationship(
        back_populates="receipt",
        cascade="all, delete-orphan",  # Удаляет посты при удалении пользователя
    )
