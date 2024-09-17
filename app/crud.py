from sqlalchemy.orm import Session
from sqlalchemy import select, exc
from fastapi import HTTPException, status
from . import models, schemas


def getCatalog(db: Session) -> dict[str, dict[int, schemas.Vegetable]]:
    return {
        "catalog": {
            vegetable.id: schemas.Vegetable.model_validate(vegetable).model_dump()
            for vegetable in db.query(models.Vegetable).all()
        }
    }


def createCatalog(db: Session):
    VEGETABLES = ["Tomato", "Onion", "Ginger", "Spinach", "Garlic", "Chilli", "Lemon"]
    for vegetableName in VEGETABLES:
        vegetable = models.Vegetable(name=vegetableName)
        db.add(vegetable)
    db.commit()


def addItem(db: Session, part_id: int, item: schemas.Item) -> HTTPException:
    Item = models.Item(vegetable_id=item.vegetableId, price=item.price)
    try:
        partner = db.query(models.Partner).filter(models.Partner.id == part_id).one()
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="partner not found"
        )

    if not partner.cart:
        cartItem = models.Cart(partner_id=part_id)
        partner.cart = cartItem
        db.add(partner.cart)

    partner.cart.items.append(Item)
    db.commit()


def getAllItems(db: Session, partnerId: int) -> dict[str, schemas.Cart] | HTTPException:
    try:
        partner = db.get_one(models.Partner, partnerId)
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="partner not found"
        )

    items = [
        schemas.Item.model_validate(item)
        for item in db.query(models.Item)
        .where(models.Item.cart_id == partner.cart.id)
        .all()
    ]
    return {"items": items}


def delItem(db: Session, partnerId: int, vegetable_id: int) -> HTTPException:
    try:
        partner = db.query(models.Partner).where(models.Partner.id == partnerId).one()
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="partner not found"
        )

    for i in range(len(partner.cart.items)):
        if partner.cart.items[i].vegetable_id == vegetable_id:
            db.delete(partner.cart.items[i])
            db.commit()
            return getAllItems(db, partnerId)

    return getAllItems(db, partnerId)


def createPartner(db: Session, partner: schemas.PartnerCreate) -> int:
    db_partner = models.Partner(name=partner.name)
    db.add(db_partner)
    db.commit()
    db_cart = models.Cart(partner=db_partner)
    db.add(db_cart)
    db.commit()
    return db_partner.id


def createUserSession(db: Session, session_id: str, user_id: int):
    db_user = db.get(models.User, user_id)
    db_user_session = models.UserSession(id=session_id, user_id=db_user.id)
    db.add(db_user_session)
    db.commit()
