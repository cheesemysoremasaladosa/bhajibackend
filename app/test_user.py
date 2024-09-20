from fastapi.testclient import TestClient
from fastapi import status
from .main import app
from .utils import initDevUserDB
from . import schemas
from pydantic import ValidationError

client = TestClient(app)

initDevUserDB()


def test_partner_list():
    response = client.get("/partners", params={"radius": 5})
    assert response.status_code == status.HTTP_200_OK
    partners_json = response.json()
    try:
        partners = schemas.PartnerList.model_validate_json(partners_json)
    except ValidationError:
        raise AssertionError("maybe an invalid response from /partners")
    assert partners == schemas.PartnerList(
        partners=[
            schemas.Partner(id=1, name="Ramesh"),
            schemas.Partner(id=2, name="Suresh"),
        ]
    )
