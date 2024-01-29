from uuid import UUID

from sqlalchemy.orm import Session

from .conftest import client
from .. import crud, schemas


class TestMenuRouts:
    def test_read_menus(self, session: Session, menu):
        response = client.get(
            "/api/v1/menus/",
        )

        assert response.status_code == 200
        data = response.json()

        db_menus = crud.get_menus(session)
        assert len(data) == len(db_menus) == 1

    def test_read_menu(self, session: Session, menu):
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
