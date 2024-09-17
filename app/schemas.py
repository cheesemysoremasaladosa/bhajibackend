from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class PartnerCreate(BaseModel):
    name: str

class Vegetable(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str

class Item(BaseModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(
        serialization_alias=to_camel
    ), from_attributes=True)
    #id: int
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


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    import models

    engine = create_engine("sqlite://")
    models.Base.metadata.create_all(engine)
    with Session(engine) as session:
        partner = models.Partner(name="Partner")
        tomato = models.Vegetable(name="Tomato")
        onion = models.Vegetable(name="Onion")
        session.add_all([partner, tomato, onion])
        session.commit()
        cart = models.Cart(partner=partner)
        session.add(cart)
        session.commit()
        session.add(models.Item(vegetable_id=tomato.id, price=23.3, cart=cart))
        session.add(models.Item(vegetable_id=onion.id, price=53.3, cart=cart))
        session.commit()
        cartData = {"items": {item.id: Item.model_validate(
            item).model_dump(by_alias=True) for item in cart.items}}
        import json
        print(json.dumps(cartData))
