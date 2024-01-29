import pytest

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app import models, schemas, crud
from app.database import SessionLocal, engine
from app.main import app

client = TestClient(app)


@pytest.fixture
def session():
    models.Base.metadata.create_all(bind=engine)

    db_session = SessionLocal()

    yield db_session

    db_session.close()
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def menu(session: Session):
    menu_data = {
        "title": "Menu 1",
        "description": "Menu 1 description"
    }

    db_menu = crud.create_menu(
        session,
        schemas.MenuCreate(**menu_data)
    )
    yield db_menu

    crud.delete_menu(session, db_menu.id)


@pytest.fixture
def submenu(session: Session, menu):
    submenu_data = {
        "title": "Submenu 1",
        "description": "Submenu 1 description"
    }

    db_submenu = crud.create_submenu(
        session,
        menu.id,
        schemas.SubmenuCreate(**submenu_data)
    )
    yield db_submenu

    crud.delete_submenu(session, db_submenu.id)


@pytest.fixture
def dish(session: Session, menu, submenu):
    dish_data = {
        "title": "Dish 1",
        "description": "Dish 1 description",
        "price": "12.50"
    }

    db_dish = crud.create_dish(
        session,
        submenu.id,
        schemas.DishCreate(**dish_data)
    )
    yield db_dish

    crud.delete_dish(session, db_dish.id)
