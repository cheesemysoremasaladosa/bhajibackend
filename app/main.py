from typing import Annotated
from fastapi import Depends, FastAPI, Header
from sqlalchemy.orm import Session
from .utils import get_db, initDevPartnerDB, verifyUserAuth
from . import crud, models, schemas
from .database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

initDevPartnerDB()


@app.get("/catalog")
def get_catalog(db: Session = Depends(get_db)):
    return crud.getCatalog(db)


@app.get("/cart/{partner_id}")
def get_cart(partner_id: int, db: Session = Depends(get_db)):
    return crud.getAllItems(db, partner_id)


# FIXME:  change endopint
@app.put("/cart/{partner_id}")
def addItem(
    partner_id: int,
    item: schemas.ItemCreate,
    sessionId: Annotated[str, Header()],
    db: Session = Depends(get_db),
):
    verifyUserAuth(db=db, user_id=partner_id, session_id=sessionId)
    return crud.addItem(db, partner_id, item)


@app.delete("/cart/{partner_id}")
def delItem(
    partner_id: int,
    sessionId: Annotated[str, Header()],
    vegetable: schemas.ItemDelete,
    db: Session = Depends(get_db),
):
    verifyUserAuth(db=db, user_id=partner_id, session_id=sessionId)
    return crud.delItem(db, partner_id, vegetable.vegetableId)
