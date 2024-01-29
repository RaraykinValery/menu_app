from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from main import app
import models
import crud
import schemas
from database import SessionLocal, engine
from operations import get_menus_with_submenus_and_dishes_counts

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


class TestMenuRouts:
    def test_read_menus(self, session: Session, menu):
        response = client.get(
            "/api/v1/menus/",
        )

        assert response.status_code == 200
        data = response.json()

        db_menus = crud.get_menus(session)
        assert len(data) == len(db_menus) == 1

    def test_read_menu(self, session: Session, menu: models.Menu):
        response = client.get(
            f"/api/v1/menus/{menu.id}"
        )
        assert response.status_code == 200
        menu_data = response.json()
        assert "id" in menu_data

        db_menu = crud.get_menu(session, UUID(menu_data["id"]))
        assert db_menu is not None

        assert menu_data["title"] == db_menu.title
        assert menu_data["description"] == db_menu.description

    def test_create_menu(self, session: Session):
        response = client.post(
            "/api/v1/menus/",
            json={
                "title": "Menu 1",
                "description": "Menu 1 description"
            }
        )
        assert response.status_code == 201
        menu_data = response.json()
        assert "id" in menu_data

        db_menu = crud.get_menu(session, UUID(menu_data["id"]))
        assert db_menu is not None

        assert menu_data["title"] == db_menu.title == "Menu 1"
        assert (menu_data["description"]
                == db_menu.description
                == "Menu 1 description")

    def test_update_menu(self, session: Session, menu):
        response = client.patch(
            f"/api/v1/menus/{menu.id}",
            json={
                "title": "Updated Menu 1",
                "description": "Updated Menu 1 description"
            }
        )
        assert response.status_code == 200
        menu_data = response.json()
        assert "id" in menu_data
        assert menu_data["title"] == "Updated Menu 1"
        assert menu_data["description"] == "Updated Menu 1 description"

        response = client.get(
            f"/api/v1/menus/{menu.id}"
        )
        assert response.status_code == 200
        menu_data = response.json()

        assert "id" in menu_data
        assert menu_data["title"] == "Updated Menu 1"
        assert menu_data["description"] == "Updated Menu 1 description"

    def test_delete_menu(self, session: Session):
        menu_data = {
            "title": "Menu 1",
            "description": "Menu 1 description"
        }

        menu = crud.create_menu(
            session,
            schemas.MenuCreate(**menu_data)
        )

        response = client.delete(
            f"/api/v1/menus/{menu.id}",
        )
        assert response.status_code == 200
        menu_data = response.json()
        assert "id" in menu_data

        assert menu_data["title"] == menu.title
        assert menu_data["description"] == menu.description

        response = client.get(
            f"/api/v1/menus/{menu.id}"
        )
        assert response.status_code == 404


class TestSubmenuRouts:
    def test_read_submenus(self, session: Session, submenu):
        response = client.get(
            f"/api/v1/menus/{submenu.menu.id}/submenus",
        )

        assert response.status_code == 200
        data = response.json()

        db_submenus = crud.get_submenus(session, submenu.menu.id)
        assert len(data) == len(db_submenus) == 1

    def test_read_submenu(self, session: Session, submenu):
        response = client.get(
            f"/api/v1/menus/{submenu.menu.id}/submenus/{submenu.id}"
        )
        assert response.status_code == 200
        submenu_data = response.json()
        assert "id" in submenu_data

        db_submenu = crud.get_submenu(session, UUID(submenu_data["id"]))
        assert db_submenu is not None

        assert submenu_data["title"] == db_submenu.title
        assert submenu_data["description"] == db_submenu.description

    def test_create_submenu(self, session: Session, menu):
        response = client.post(
            f"/api/v1/menus/{menu.id}/submenus",
            json={
                "title": "Submenu 1",
                "description": "Submenu 1 description"
            }
        )
        assert response.status_code == 201
        submenu_data = response.json()
        assert "id" in submenu_data

        db_submenu = crud.get_submenu(session, UUID(submenu_data["id"]))
        assert db_submenu is not None

        assert submenu_data["title"] == db_submenu.title
        assert submenu_data["description"] == db_submenu.description

    def test_update_submenu(self, session: Session, submenu):
        response = client.patch(
            f"/api/v1/menus/{submenu.menu.id}/submenus/{submenu.id}",
            json={
                "title": "Updated Submenu 1",
                "description": "Updated Submenu 1 description"
            }
        )
        assert response.status_code == 200
        submenu_data = response.json()
        assert "id" in submenu_data
        assert submenu_data["title"] == "Updated Submenu 1"
        assert submenu_data["description"] == "Updated Submenu 1 description"

        response = client.get(
            f"/api/v1/menus/{submenu.menu.id}/submenus/{submenu.id}",
        )
        assert response.status_code == 200
        submenu_data = response.json()
        assert "id" in submenu_data
        assert submenu_data["title"] == "Updated Submenu 1"
        assert submenu_data["description"] == "Updated Submenu 1 description"

    def test_delete_submenu(self, session: Session, menu):
        submenu_data = {
            "title": "Submenu 1",
            "description": "Submenu 1 description"
        }

        submenu = crud.create_submenu(
            session,
            menu.id,
            schemas.SubmenuCreate(**submenu_data)
        )

        response = client.delete(
            f"/api/v1/menus/{submenu.menu.id}/submenus/{submenu.id}",
        )
        assert response.status_code == 200
        submenu_data = response.json()
        assert "id" in submenu_data

        assert submenu_data["title"] == submenu.title
        assert submenu_data["description"] == submenu.description

        response = client.get(
            f"/api/v1/menus/{submenu.menu.id}/submenus/{submenu.id}",
        )
        assert response.status_code == 404


class TestDishRouts:
    def test_read_dishes(self, session: Session, dish):
        response = client.get(
            f"/api/v1/menus/{dish.submenu.menu.id}"
            f"/submenus/{dish.submenu.id}/dishes",
        )

        assert response.status_code == 200
        data = response.json()

        db_dishes = crud.get_dishes(session, dish.submenu.id)
        assert len(data) == len(db_dishes) == 1

    def test_read_dish(self, session: Session, dish):
        response = client.get(
            f"/api/v1/menus/{dish.submenu.menu.id}"
            f"/submenus/{dish.submenu.id}/dishes/{dish.id}"
        )
        assert response.status_code == 200
        dish_data = response.json()
        assert "id" in dish_data

        db_dish = crud.get_dish(session, UUID(dish_data["id"]))
        assert db_dish is not None

        assert dish_data["title"] == db_dish.title
        assert dish_data["description"] == db_dish.description
        assert dish_data["price"] == db_dish.price

    def test_create_dish(self, session: Session, submenu):
        response = client.post(
            (
                f"/api/v1/menus/{submenu.menu.id}"
                f"/submenus/{submenu.id}/dishes"
            ),
            json={
                "title": "Dish 1",
                "description": "Dish 1 description",
                "price": "15.47"
            }
        )
        assert response.status_code == 201
        dish_data = response.json()
        assert "id" in dish_data

        db_dish = crud.get_dish(session, UUID(dish_data["id"]))
        assert db_dish is not None

        assert dish_data["title"] == db_dish.title
        assert dish_data["description"] == db_dish.description
        assert dish_data["price"] == db_dish.price

    def test_update_dish(self, session: Session, dish):
        response = client.patch(
            (
                f"/api/v1/menus/{dish.submenu.menu.id}"
                f"/submenus/{dish.submenu.id}/dishes/{dish.id}"
            ),
            json={
                "title": "Updated Dish 1",
                "description": "Updated Dish 1 description"
            }
        )
        assert response.status_code == 200
        dish_data = response.json()
        assert "id" in dish_data
        assert dish_data["title"] == "Updated Dish 1"
        assert dish_data["description"] == "Updated Dish 1 description"

        response = client.get(
            f"/api/v1/menus/{dish.submenu.menu.id}"
            f"/submenus/{dish.submenu.id}/dishes/{dish.id}"
        )
        assert response.status_code == 200
        dish_data = response.json()
        assert "id" in dish_data
        assert dish_data["title"] == "Updated Dish 1"
        assert dish_data["description"] == "Updated Dish 1 description"

    def test_delete_dish(self, session: Session, menu, submenu):
        dish_data = {
            "title": "Dish 1",
            "description": "Dish 1 description",
            "price": "12.50"
        }

        dish = crud.create_dish(
            session,
            submenu.id,
            schemas.DishCreate(**dish_data)
        )

        response = client.delete(
            f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}",
        )
        assert response.status_code == 200
        dish_data = response.json()
        assert "id" in dish_data

        assert dish_data["title"] == dish.title
        assert dish_data["description"] == dish.description
        assert dish_data["price"] == dish.price

        response = client.get(
            f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}",
        )
        assert response.status_code == 404


def test_submenus_and_dishes_count(session: Session):
    # Создаёт меню
    response = client.post(
        "/api/v1/menus/",
        json={
            "title": "Menu 1",
            "description": "Menu 1 description"
        }
    )
    assert response.status_code == 201
    menu_data = response.json()
    assert "id" in menu_data

    # Создаёт подменю
    response = client.post(
        f"/api/v1/menus/{menu_data['id']}/submenus",
        json={
            "title": "Submenu 1",
            "description": "Submenu 1 description"
        }
    )
    assert response.status_code == 201
    submenu_data = response.json()
    assert "id" in submenu_data

    # Создаёт блюдо 1
    response = client.post(
        (
            f"/api/v1/menus/{menu_data['id']}"
            f"/submenus/{submenu_data['id']}/dishes"
        ),
        json={
            "title": "Dish 1",
            "description": "Dish 1 description",
            "price": "15.47"
        }
    )
    assert response.status_code == 201
    dish_data = response.json()
    assert "id" in dish_data

    # Создаёт блюдо 2
    response = client.post(
        (
            f"/api/v1/menus/{menu_data['id']}"
            f"/submenus/{submenu_data['id']}/dishes"
        ),
        json={
            "title": "Dish 2",
            "description": "Dish 2 description",
            "price": "20.45"
        }
    )
    assert response.status_code == 201
    dish_data = response.json()
    assert "id" in dish_data

    # Просматривает определённое меню
    response = client.get(
        f"/api/v1/menus/{menu_data['id']}"
    )
    assert response.status_code == 200
    menu_read_data = response.json()
    assert menu_read_data['id'] == menu_data['id']
    menu_with_counts = get_menus_with_submenus_and_dishes_counts(
        session, UUID(menu_data['id']))
    assert menu_read_data['submenus_count'] == menu_with_counts.submenus_count
    assert menu_read_data['dishes_count'] == menu_with_counts.dishes_count

    # Просматривает определённое подменю
    response = client.get(
        f"/api/v1/menus/{menu_data['id']}/submenus/{submenu_data['id']}"
    )
    assert response.status_code == 200
    submenu_read_data = response.json()
    assert submenu_read_data['id'] == submenu_data['id']
    assert submenu_read_data['dishes_count'] == 2

    # Удаляет подменю
    response = client.delete(
        f"api/v1/menus/{menu_data['id']}/submenus/{submenu_data['id']}"
    )
    assert response.status_code == 200

    # Просматривает список подменю
    response = client.get(
        f"api/v1/menus/{menu_data['id']}/submenus"
    )
    assert response.status_code == 200
    assert response.json() == []

    # Просматривает список блюд
    response = client.get(
        f"api/v1/menus/{menu_data['id']}/submenus/{submenu_data['id']}/dishes"
    )
    assert response.status_code == 200
    assert response.json() == []

    # Просматривает определённое меню
    response = client.get(
        f"api/v1/menus/{menu_data['id']}"
    )
    assert response.status_code == 200
    menu_read_data = response.json()
    assert menu_read_data['id'] == menu_data['id']
    assert menu_read_data['submenus_count'] == 0
    assert menu_read_data['dishes_count'] == 0

    # Удаляет меню
    response = client.delete(
        f"api/v1/menus/{menu_data['id']}"
    )
    assert response.status_code == 200

    # Просматривает список меню
    response = client.get("api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []
