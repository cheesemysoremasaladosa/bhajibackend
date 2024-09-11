from peewee import *

db = SqliteDatabase('bhaji.db')

class User(Model):
    name = CharField()
    class Meta:
        database = db

class Session(Model):
    id = UUIDField(primary_key=True)
    user = ForeignKeyField(User, backref='sessions')

    class Meta:
        database = db

class Partner(Model):
    user = ForeignKeyField(User, backref='partner')
    class Meta:
        database = db

class Cart(Model):
    partner = ForeignKeyField(Partner, backref='cart')

    class Meta:
        database = db

class Vegetable(Model):
    name = CharField()
    
    class Meta:
        database = db

class Item(Model):
    vegetable = ForeignKeyField(Vegetable)
    cart = ForeignKeyField(Cart, backref='items')
    price = FloatField()

    class Meta:
        database = db