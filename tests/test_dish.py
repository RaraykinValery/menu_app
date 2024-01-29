from uuid import UUID

from sqlalchemy.orm import Session

from tests.conftest import client
from app import crud, schemas


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
