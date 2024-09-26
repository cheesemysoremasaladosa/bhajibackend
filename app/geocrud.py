import redis.asyncio as redis
from . import schemas

async def addPartnerLocation(geodb: redis.Redis, location: schemas.PartnerLocation):
    pass

async def getPartnersFromPos(geodb, radius: int, lat: float, lon: float)->schemas.PartnerLocation:
    pass