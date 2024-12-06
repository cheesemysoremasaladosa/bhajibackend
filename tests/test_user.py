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
    response = client.get("/partners", params={"radius": 10, "lat": 18.588506286852226, "lon": 73.82248587694585})
    assert response.status_code == status.HTTP_200_OK
    partners_json = response.json()
    partners_list = schemas.PartnerList.model_validate(partners_json)
    assert [located_partner.partner.name for located_partner in partners_list.partners] == ["Suresh","Ramesh"]