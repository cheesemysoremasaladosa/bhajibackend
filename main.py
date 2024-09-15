from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session


import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def catalogCreate():
    db = next(get_db())
    crud.createCatalog(db)

catalogCreate()

@app.get("/catalog")
def get_catalog(db:Session=Depends(get_db)):
    return crud.getCatalog(db)

@app.get("/get-cart/{partner_id}")
def get_cart(partner_id:int,db:Session=Depends(get_db)):
    return crud.getAllItems(db,partner_id)

# FIXME:  change endopint
@app.put("/cart/{partner_id}")
def addItem(partner_id: int,item: schemas.ItemCreate,db: Session= Depends(get_db)):
    return crud.addItem(db,partner_id,item)

@app.delete("/cart/{partner_id}")
def delItem(partner_id: int,vegetable :schemas.ItemDelete,db: Session= Depends(get_db)):
    return crud.delItem(db,partner_id,vegetable.vegetableId)

@app.put("/new-user/")
def add_newuser(user: schemas.UserCreate,db: Session= Depends(get_db)):
    return crud.addUser(db,user)


@app.put("/new-partner/")
def add_new_partner(partner_id: schemas.PartnerCreate,db: Session= Depends(get_db)):
    return crud.addPartner(db,partner_id)