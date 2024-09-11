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
    query = Item.delete().where(cart=cartId).where(vegetable = vegetableId)
    query.execute()

def createCatalog():
    vegetables = ["Tomato", "Onion", "Carrot"]
    for vegetable in vegetables:
        Vegetable.create(name=vegetable)

def getCatalog():
    return {"catalog": [{"name": vegetable.name} for vegetable in Vegetable.select()]}

if __name__ == '__main__':
    createCatalog()