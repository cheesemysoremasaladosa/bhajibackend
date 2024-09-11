from models import *

db = SqliteDatabase('bhaji.db')

def createTables():
    db.create_tables([User, Session, Vegetable, Partner, Cart, Item])

def createPartner(name: str)->int:
    user = User.create(name=name)
    partner = Partner.create(user=user)
    Cart.create(partner=partner)
    return partner.id

def createItem(cartId: int, vegetableId: int, price: float):
    return Item.create(cart=cartId, vegetable=vegetableId, price=price)

def removeItem(cartId: int, vegetableId: int):
    Item.delete().where(Item.cart==cartId and Item.vegetable == vegetableId).execute()

def addItemToCart(partnerId: int, vegetableId: int, price: float):
    cart = Cart.get_or_none(partner=partnerId)
    if not cart:
        return Exception("invalid partnerId")
    createItem(cartId=cart.id, vegetableId=vegetableId, price=price)

def removeItemFromCart(partnerId: int, vegetableId: int):
    cart = Cart.get_or_none(partner=partnerId)
    if not cart:
        return Exception("invalid partnerId")
    removeItem(cartId=cart.id, vegetableId=vegetableId)

def getPartnerCart(partnerId: int):
    cart = Cart.get_or_none(partner=partnerId)
    if not cart:
        return Exception("invalid partnerId")
    items = {item.vegetable_id: {"price": item.price} for item in cart.items}
    return {"items": items}

def createCatalog():
    vegetables = ["Tomato", "Onion", "Carrot"]
    for vegetable in vegetables:
        Vegetable.create(name=vegetable)

def getCatalog():
    return {"catalog": {vegetable.id:{"name": vegetable.name} for vegetable in Vegetable.select()}}

if __name__ == '__main__':
    createCatalog()