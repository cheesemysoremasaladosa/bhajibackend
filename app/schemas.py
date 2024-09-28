from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel
from pydantic_extra_types.coordinate import Latitude, Longitude
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
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
    name: str

class PartnerLocation(BaseModel):
    partnerId: int
    lat: Latitude
    lon: Longitude

class LocatedPartner(BaseModel):
    partner: Partner
    lat: Latitude
    lon: Longitude

class PartnerList(BaseModel):
    partners: list[LocatedPartner]