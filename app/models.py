from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str]

    sessions = relationship("UserSession", back_populates="user")
    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": "type"}


class UserSession(Base):
    __tablename__ = "user_session"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="sessions")


class Partner(User):
    __tablename__ = "partner"
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    cart = relationship("Cart", uselist=False, back_populates="partner")
    __mapper_args__ = {"polymorphic_identity": "partner"}


class Vegetable(Base):
    __tablename__ = "vegetable"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)


class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    partner_id = mapped_column(Integer, ForeignKey("partner.id"))

    partner = relationship("Partner", back_populates="cart")
    items = relationship("Item", back_populates="cart")


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    price: Mapped[float] = mapped_column(Float)
    vegetable_id: Mapped[int] = mapped_column(Integer, ForeignKey("vegetable.id"))
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("cart.id"))

    cart = relationship("Cart", back_populates="items")
