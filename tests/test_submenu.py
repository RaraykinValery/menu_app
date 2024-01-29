from uuid import UUID

from sqlalchemy.orm import Session

from .conftest import client
from .. import crud, schemas


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
