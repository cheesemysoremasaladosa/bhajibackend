from sqlalchemy.orm import Session,exc
from sqlalchemy import select
import models, schemas


def getCatalog(db: Session)->dict[str, dict[int, schemas.Vegetable]]:
    return {"catalog": {vegetable.id: schemas.Vegetable.model_validate(vegetable).model_dump() for vegetable in db.query(models.Vegetable).all()}}

def createCatalog(db: Session):
    VEGETABLES = ["Tomato", "Onion", "Ginger", "Spinach", "Garlic", "Chilli", "Lemon"]
    for vegetableName in VEGETABLES:
        vegetable = models.Vegetable(name=vegetableName)
        db.add(vegetable)
    db.commit()

def addItem(db: Session,part_id :int ,item: schemas.Item):
    Item = models.Item(vegetable_id=item.vegetableId,price=item.price)
    try:
        partner = db.query(models.Partner).filter(models.Partner.id == part_id).one()
    except exc.NoResultFound:
        return {
            "Error":True,
            "From":"addItem",
            "Status":f"No partner found with partner id {part_id}"
        }
    
    if not partner.cart:
        cartItem = models.Cart(partner_id=part_id)
        partner.cart = cartItem
        db.add(partner.cart)
    partner.cart.items.append(Item)
    db.commit()
    return {
        "Error":False,
        "Status":"new item added"
    }

def getAllItems(db:Session,partnerId: int):
    allitems = db.query(models.Partner).where(models.Partner.id==partnerId).one()
    return {"items": {i.id: schemas.Item.model_validate(i).model_dump() for i in allitems.cart.items}}



def addUser(db: Session,user : schemas.UserCreate):
    user = models.User(name=user.name,type=user.type)
    db.add(user)
    db.commit()
    print(db.query(models.User).all())

def addPartner(db: Session,partner: schemas.PartnerCreate):
    partner = models.Partner(name=partner.name)
    db.add(partner)
    db.commit()
    return {
        "Error":False,
        "Status":f"partner id is {partner.id}",
    }
