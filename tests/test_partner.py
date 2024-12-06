from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.utils import initDevPartnerDB, get_db
from app.crud import getCatalog
from app.database import engine
from app import models
from app import schemas

client = TestClient(app)
models.Base.metadata.create_all(bind=engine)
initDevPartnerDB()

catalog = getCatalog(db=next(get_db()))["catalog"]

DEV_SESSION_ID = "e3e70682-c209-4cac-a29f-6fbed82c07cd"
DEV_PARTNER_ID = 1


def test_cart():
    # test cart ops get, put, delete

    response = client.get(f"/cart/{DEV_PARTNER_ID}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"items": []}

    item = schemas.ItemCreate(vegetableId=1, price=23.0).model_dump()
    response = client.put(
        f"/cart/{DEV_PARTNER_ID}",
        json=item,
        headers={"SessionID": DEV_SESSION_ID},
    )
    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/cart/{DEV_PARTNER_ID}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"items": [item]}

    item = schemas.ItemDelete(vegetableId=1).model_dump()
    # TestClient doesn't support json payload for delete method, manually create a request
    # response = client.delete(f"/cart/{DEV_PARTNER_ID}", json=item, headers={"SessionID":DEV_SESSION_ID})
    response = client.request(
        "DELETE",
        url=f"/cart/{DEV_PARTNER_ID}",
        json=item,
        headers={"SessionID": DEV_SESSION_ID},
    )
    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/cart/{DEV_PARTNER_ID}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"items": []}


def test_cart_errors():
    partner_id = 4  # wrong partner_id
    response = client.get(f"/cart/{partner_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_cart_auth():
    item = schemas.ItemCreate(vegetableId=1, price=23.0).model_dump()
    WRONG_SESSION_ID = "3240123"
    response = client.put(
        f"/cart/{DEV_PARTNER_ID}",
        json=item,
        headers={"SessionID": WRONG_SESSION_ID},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    item = schemas.ItemDelete(vegetableId=1).model_dump()
    # TestClient doesn't support json payload for delete method, manually create a request
    # response = client.delete(f"/cart/{DEV_PARTNER_ID}", json=item, headers={"SessionID":DEV_SESSION_ID})
    response = client.request(
        "DELETE",
        url=f"/cart/{DEV_PARTNER_ID}",
        json=item,
        headers={"SessionID": WRONG_SESSION_ID},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
