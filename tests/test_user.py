from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.utils import initDevUserDB
from app import schemas, models
from app.database import engine
import pytest

client = TestClient(app)

@pytest.fixture()
def setup():
    models.Base.metadata.create_all(bind=engine)
    initDevUserDB()
    yield

def test_partner_list(setup):
    response = client.get("/partners", params={"radius": 100, "lat": 10.0, "lon": 10.0})
    assert response.status_code == status.HTTP_200_OK
    partners_json = response.json()
    partners = schemas.PartnerList.model_validate(partners_json)
    assert partners == schemas.PartnerList(
        partners=[
            schemas.LocatedPartner(partner=schemas.Partner(id=2, name="Ramesh"), lat=10.0, lon=10.0),
            schemas.LocatedPartner(partner=schemas.Partner(id=3, name="Suresh"), lat=11.0, lon=11.0),
        ]
    )