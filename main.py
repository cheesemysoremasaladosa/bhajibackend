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