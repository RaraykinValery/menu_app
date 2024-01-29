from uuid import UUID

from sqlalchemy.orm import Session

from tests.conftest import client
from tests.conftest import class_session as session
from app import operations


class TestSubmenusAndDishesCounts:
    menu_id = ""
    submenu_id = ""

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

        TestSubmenusAndDishesCounts.menu_id = menu_data['id']

    def test_create_submenu(self, session: Session):
        response = client.post(
            f"/api/v1/menus/{TestSubmenusAndDishesCounts.menu_id}/submenus",
            json={
                "title": "Submenu 1",
                "description": "Submenu 1 description"
            }
        )
        assert response.status_code == 201
        submenu_data = response.json()
        assert "id" in submenu_data

        TestSubmenusAndDishesCounts.submenu_id = submenu_data['id']

    def test_create_dish_1(self, session: Session):
        response = client.post(
            (
                f"/api/v1/menus/{TestSubmenusAndDishesCounts.menu_id}"
                f"/submenus/{TestSubmenusAndDishesCounts.submenu_id}/dishes"
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

    def test_create_dish_2(self, session: Session):
        response = client.post(
            (
                f"/api/v1/menus/{TestSubmenusAndDishesCounts.menu_id}"
                f"/submenus/{TestSubmenusAndDishesCounts.submenu_id}/dishes"
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

    def test_read_menu(self, session: Session):
        response = client.get(
            f"/api/v1/menus/{TestSubmenusAndDishesCounts.menu_id}"
        )
        assert response.status_code == 200
        menu_data = response.json()
        assert menu_data['id'] == TestSubmenusAndDishesCounts.menu_id
        menu_with_counts = operations.get_menu_with_submenus_and_dishes_counts(
            session, UUID(menu_data['id']))
        assert menu_data['submenus_count'] == menu_with_counts.submenus_count
        assert menu_data['dishes_count'] == menu_with_counts.dishes_count

    def test_read_submenu(self, session: Session):
        response = client.get(
            f"/api/v1/menus/{TestSubmenusAndDishesCounts.menu_id}"
            f"/submenus/{TestSubmenusAndDishesCounts.submenu_id}"
        )
        assert response.status_code == 200
        submenu_data = response.json()
        assert submenu_data['id'] == TestSubmenusAndDishesCounts.submenu_id
        assert submenu_data['dishes_count'] == 2

    def test_delete_submenu(self, session: Session):
        response = client.delete(
            f"api/v1/menus/{TestSubmenusAndDishesCounts.menu_id}"
            f"/submenus/{TestSubmenusAndDishesCounts.submenu_id}"
        )
        assert response.status_code == 200

    def test_list_submenus(self, session: Session):
        response = client.get(
            f"api/v1/menus/{TestSubmenusAndDishesCounts.menu_id}/submenus"
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_list_dishes(self, session: Session):
        response = client.get(
            f"api/v1/menus/{TestSubmenusAndDishesCounts.menu_id}"
            f"/submenus/{TestSubmenusAndDishesCounts.submenu_id}/dishes"
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_read_menu_with_no_submenus_and_dishes(self, session: Session):
        response = client.get(
            f"api/v1/menus/{TestSubmenusAndDishesCounts.menu_id}"
        )
        assert response.status_code == 200
        menu_read_data = response.json()
        assert menu_read_data['id'] == TestSubmenusAndDishesCounts.menu_id
        assert menu_read_data['submenus_count'] == 0
        assert menu_read_data['dishes_count'] == 0

    def test_delete_menu(self, session: Session):
        response = client.delete(
            f"api/v1/menus/{TestSubmenusAndDishesCounts.menu_id}"
        )
        assert response.status_code == 200

    def test_list_menus(self, session: Session):
        response = client.get("api/v1/menus")
        assert response.status_code == 200
        assert response.json() == []
