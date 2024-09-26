from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, declarative_base
import redis.asyncio as redis

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

RedisConnectionPool = redis.ConnectionPool()
Base = declarative_base()
