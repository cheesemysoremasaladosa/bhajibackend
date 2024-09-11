from dbutils import *
import os

os.remove("bhaji.db")
createTables()
createCatalog()

catalog = getCatalog()["catalog"]
partner1Id = createPartner(name= "Partner 1")
assert getPartnerCart(partner1Id) == {'items': {}}

addItemToCart(partnerId=partner1Id, vegetableId=1, price=23.3)
addItemToCart(partnerId=partner1Id, vegetableId=2, price=3.4)

assert getPartnerCart(partner1Id) == {'items': {1: {"price": 23.3}, 2: {"price": 3.4}}}

removeItemFromCart(partnerId=partner1Id, vegetableId=1)
assert getPartnerCart(partner1Id) == {'items': {2: {"price": 3.4}}}