from uuid import UUID

from app import models, schemas, services
from app.utils import reverse
from tests.conftest import client


class TestSubmenuRouts:
    def test_read_submenus_success(
            self,
            submenu: models.Submenu,
            submenu_service: services.SubmenuService
    ) -> None:
        response = client.get(
            reverse('read_submenus', menu_id=submenu.menu.id)
        )

        assert response.status_code == 200
        data = response.json()

        submenus = submenu_service.get_all(submenu.menu.id)
        assert len(data) == len(submenus) == 1

    def test_read_submenu_success(
            self,
            submenu: models.Submenu,
            submenu_service: services.SubmenuService
    ) -> None:
        response = client.get(
            reverse(
                'read_submenu',
                menu_id=submenu.menu.id,
                submenu_id=submenu.id
            )
        )
        assert response.status_code == 200
        submenu_data = response.json()
        assert 'id' in submenu_data

        submenu = submenu_service.get(
            UUID(submenu_data['menu_id']),
            UUID(submenu_data['id'])
        )
        assert submenu is not None

        assert submenu_data['title'] == submenu.title
        assert submenu_data['description'] == submenu.description

    def test_create_submenu_success(
            self,
            menu: models.Menu,
            submenu_service: services.SubmenuService
    ) -> None:
        response = client.post(
            reverse('create_submenu', menu_id=menu.id),
            json={
                'title': 'Submenu 1',
                'description': 'Submenu 1 description'
            }
        )
        assert response.status_code == 201
        submenu_data = response.json()
        assert 'id' in submenu_data

        submenu = submenu_service.get(
            UUID(submenu_data['menu_id']),
            UUID(submenu_data['id'])
        )
        assert submenu is not None

        assert submenu_data['title'] == submenu.title
        assert submenu_data['description'] == submenu.description

    def test_update_submenu_success(
            self,
            submenu: models.Submenu
    ) -> None:
        response = client.patch(
            reverse(
                'update_submenu',
                menu_id=submenu.menu.id,
                submenu_id=submenu.id
            ),
            json={
                'title': 'Updated Submenu 1',
                'description': 'Updated Submenu 1 description'
            }
        )
        assert response.status_code == 200
        submenu_data = response.json()
        assert 'id' in submenu_data
        assert submenu_data['title'] == 'Updated Submenu 1'
        assert submenu_data['description'] == 'Updated Submenu 1 description'

        response = client.get(
            reverse(
                'read_submenu',
                menu_id=submenu.menu.id,
                submenu_id=submenu.id
            ),
        )
        assert response.status_code == 200
        submenu_data = response.json()
        assert 'id' in submenu_data
        assert submenu_data['title'] == 'Updated Submenu 1'
        assert submenu_data['description'] == 'Updated Submenu 1 description'

    def test_delete_submenu_success(
            self,
            menu: models.Menu,
            submenu_service: services.SubmenuService
    ) -> None:
        submenu_data = {
            'title': 'Submenu 1',
            'description': 'Submenu 1 description'
        }

        submenu = submenu_service.create(
            menu.id,
            schemas.SubmenuCreate(**submenu_data)
        )

        response = client.delete(
            reverse(
                'delete_submenu',
                menu_id=submenu.menu.id,
                submenu_id=submenu.id
            ),
        )
        assert response.status_code == 200
        submenu_data = response.json()
        assert 'id' in submenu_data

        assert submenu_data['title'] == submenu.title
        assert submenu_data['description'] == submenu.description

        response = client.get(
            reverse(
                'read_submenu',
                menu_id=submenu.menu.id,
                submenu_id=submenu.id
            ),
        )
        assert response.status_code == 404
