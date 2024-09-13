from sqlalchemy.orm import Session
from sqlalchemy import select
import models, schemas


def getCatalog(db: Session)->dict[str, dict[int, schemas.Vegetable]]:
    return {"catalog": {vegetable.id: schemas.Vegetable.model_validate(vegetable).model_dump() for vegetable in db.query(models.Vegetable).all()}}

def createCatalog(db: Session):
    VEGETABLES = ["Tomato", "Onion", "Ginger", "Spinach", "Garlic", "Chilli", "Lemon"]
    for vegetableName in VEGETABLES:
        vegetable = models.Vegetable(name=vegetableName)
        db.add(vegetable)
    db.commit()