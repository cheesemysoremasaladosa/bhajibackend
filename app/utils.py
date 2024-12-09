from .database import SessionLocal
from . import crud, schemas, models, geocrud
import random
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import redis
from .config import settings

# REMOVE THIS IN PROD AND USE `secrets`
random.seed(0)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_geodb():
    client = redis.Redis(host=settings.redis_host, port=settings.redis_port)
    try:
        yield client
    finally:
        client.close()

def initDB():
    db = next(get_db())
    crud.createCatalog(db)
    initDevPartnerDB()
    initDevUserDB()

def initDevPartnerDB(): 
    #initialize the database for partner testing
    db = next(get_db())
    dev_user_id = crud.createPartner(
        db, partner=schemas.PartnerCreate(name="DEV_PARTNER")
    )
    dev_session_id = str(uuid.UUID(int=random.getrandbits(128), version=4))
    crud.createUserSession(db, session_id=dev_session_id, user_id=dev_user_id)
    print(f"DEV_SESSION_ID: {dev_session_id}\nDEV_USER_ID: {dev_user_id}")

def initDevUserDB():
    #initialize the database for user testing
    db = next(get_db())
    geodb = next(get_geodb())
    ramesh_id = crud.createPartner(
        db, partner=schemas.PartnerCreate(name="Ramesh")
    )
    geocrud.addPartnerLocation(geodb=geodb, location=schemas.PartnerLocation(partnerId=ramesh_id, lat=18.58791783341944, lon=73.8279781974082))
    suresh_id = crud.createPartner(
        db, partner=schemas.PartnerCreate(name="Suresh")
    )
    geocrud.addPartnerLocation(geodb=geodb, location=schemas.PartnerLocation(partnerId=suresh_id, lat=18.586205319964993, lon=73.81610851701967))

def verifyUserAuth(db: Session, user_id: int, session_id: str) -> HTTPException | None:
    try:
        db.query(models.UserSession).where(
            models.UserSession.user_id == user_id, models.UserSession.id == session_id
        ).one()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="bad session id or partner id",
        )
