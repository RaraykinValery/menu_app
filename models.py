import uuid

from sqlalchemy import Column, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from database import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Uuid, primary_key=True, unique=True,
                default=uuid.uuid4)
    title = Column(String, unique=True)
    description = Column(Text)
    price = Column(String)

    submenu_id = Column(Uuid, ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Uuid, primary_key=True, unique=True,
                default=uuid.uuid4)
    title = Column(String, unique=True)
    description = Column(Text)

    menu_id = Column(Uuid, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu",
                          cascade="all, delete-orphan")

    @hybrid_property
    def dishes_count(self):
        return len(self.dishes)


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Uuid, primary_key=True, unique=True,
                default=uuid.uuid4)
    title = Column(String, unique=True)
    description = Column(Text)

    submenus = relationship(
        "Submenu", back_populates="menu", cascade="all, delete-orphan")

    @hybrid_property
    def submenus_count(self):
        return len(self.submenus)

    @hybrid_property
    def dishes_count(self):
        return sum(len(submenu.dishes) for submenu in self.submenus)
