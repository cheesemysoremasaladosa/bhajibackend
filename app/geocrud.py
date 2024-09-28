import redis
from fastapi import HTTPException
from . import schemas, crud, models
from typing import *

def addPartnerLocation(
    geodb: redis.Redis, location: schemas.PartnerLocation
) -> None | HTTPException:
    # TODO: validate lat and lon
    geodb.geoadd("Partners", [location.lon, location.lat, location.partnerId])


def getPartnersFromPos(
    db, geodb: redis.Redis, radius: int, lat: float, lon: float
) -> schemas.PartnerLocation:
    # TODO: validate lat and lon
    geovalues: List[Tuple[bytes, float, (float, float)]] = geodb.geosearch(
        name="Partners",
        radius=radius,
        longitude=lon,
        latitude=lat,
        unit="km",
        withcoord=True,
        withdist=True,
    )

    partners = []
    for geovalue in geovalues:
        partnerId, distance, (lat, lon) = geovalue
        partnerId = int(partnerId)  # redis returns bytes object for key
        partner: schemas.Partner = crud.getPartnerById(db=db,partner_id=partnerId)
        partners.append(schemas.LocatedPartner(partner=partner, lat=lat, lon=lon, distance=distance))

    return schemas.PartnerList(partners=partners)