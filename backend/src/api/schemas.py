from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class QrSchema(BaseModel):
    data: str = Field(pattern=r"t=[\dT]+&s=\d+.\d{2}&fn=\d+&i=\d+&fp=\d+&n=\d")


class OFDItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    price: int
    quantity: float
    items_quantity_measure: int | None = Field(
        default=None, validation_alias=AliasChoices("itemsQuantityMeasure")
    )


class OFDReceiptSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    qrraw: str

    user: str
    user_inn: str = Field(..., validation_alias=AliasChoices("userInn"))
    seller_address: str | None = Field(
        default=None, validation_alias=AliasChoices("sellerAddress")
    )
    retail_place: str = Field(..., validation_alias=AliasChoices("retailPlace"))
    retail_place_address: str | None = Field(
        default=None, validation_alias=AliasChoices("retailPlaceAddress")
    )
    region: str
    date_time: datetime = Field(..., validation_alias=AliasChoices("dateTime"))
    credit_sum: int = Field(..., validation_alias=AliasChoices("creditSum"))
    code: int
    operation_type: int = Field(..., validation_alias=AliasChoices("operationType"))
    total_sum: int = Field(..., validation_alias=AliasChoices("totalSum"))
    buyer_phone_or_address: str | None = Field(
        default=None, validation_alias=AliasChoices("buyerPhoneOrAddress")
    )
    items: list[OFDItemSchema]


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
