from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship

from .database import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    description = Column(Text)
    price = Column(Float)

    submenu_id = Column(Integer, ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    description = Column(Text)

    menu_id = Column(Integer, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu",
                          cascade="all, delete-orphan")


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    description = Column(Text)

    submenus = relationship(
        "Submenu", back_populates="menu", cascade="all, delete-orphan")
