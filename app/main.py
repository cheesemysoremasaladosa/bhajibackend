from contextlib import asynccontextmanager
import logging.config
from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy.orm import Session
import redis.asyncio as redis
from .utils import get_db, get_geodb, initDevPartnerDB, verifyUserAuth
from . import crud, geocrud, models, schemas
from .database import engine
from .config import settings
import logging

log: logging.Logger = logging.getLogger("uvicorn.default")

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    initDevPartnerDB()
    yield


app = FastAPI(lifespan=lifespan)


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
    return crud.addItem(db, partner_id, item=item)


@app.delete("/cart/{partner_id}")
def delItem(
    partner_id: int,
    sessionId: Annotated[str, Header()],
    vegetable: schemas.ItemDelete,
    db: Session = Depends(get_db),
):
    verifyUserAuth(db=db, user_id=partner_id, session_id=sessionId)
    return crud.delItem(db, partner_id, vegetable.vegetableId)


@app.get("/partners")
async def getPartners(
    radius: int,
    lat: float,
    lon: float,
    db: Session = Depends(get_db),
    geodb: redis.Redis = Depends(get_geodb),
):
    return await geocrud.getPartnersFromPos(
        db=db, geodb=geodb, radius=radius, lat=lat, lon=lon
    )


@app.post("/partner/location")
async def postLocation(
    location: schemas.PartnerLocation,
    sessionId: Annotated[str, Header()],
    db: Session = Depends(get_db),
    geodb: redis.Redis = Depends(get_geodb),
):
    #verifyUserAuth(db=db, user_id=location.partnerId, session_id=sessionId)
    await geocrud.addPartnerLocation(geodb=geodb, location=location)