from .database import SessionLocal
from . import crud, schemas, models
import random
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import exc

# REMOVE THIS IN PROD AND USE `secrets`
random.seed(0)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initDevDB():
    db = next(get_db())
    crud.createCatalog(db)
    dev_user_id = crud.createPartner(
        db, partner=schemas.PartnerCreate(name="DEV_PARTNER")
    )
    dev_session_id = str(uuid.UUID(int=random.getrandbits(128), version=4))
    crud.createUserSession(db, session_id=dev_session_id, user_id=dev_user_id)
    print(f"DEV_SESSION_ID: {dev_session_id}\nDEV_USER_ID: {dev_user_id}")


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
