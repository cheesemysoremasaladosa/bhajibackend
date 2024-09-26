from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class PartnerCreate(BaseModel):
    name: str


class Vegetable(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class Item(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=to_camel),
        from_attributes=True,
    )
    # id: int
    vegetable_id: int
    price: float


class ItemCreate(BaseModel):
    vegetableId: int
    price: float


class ItemDelete(BaseModel):
    vegetableId: int


class UserCreate(BaseModel):
    name: str
    type: str


class Cart(BaseModel):
    items: list[Item]

class Partner(BaseModel):
    id: int
    name: str

class PartnerList(BaseModel):
    partners: list[Partner]