from uuid import UUID

from app import schemas
from app.utils import reverse
from tests.conftest import client


class TestMenuRouts:
    def test_read_menus_success(self, menu, menu_service):
        response = client.get(
            reverse('read_menus')
        )

        assert response.status_code == 200
        data = response.json()

        menus = menu_service.get_all()
        assert len(data) == len(menus) == 1

    def test_read_menu_success(self, menu, menu_service):
        response = client.get(
            reverse('read_menu', menu_id=menu.id)
        )
        assert response.status_code == 200
        menu_data = response.json()
        assert 'id' in menu_data

        menu = menu_service.get(UUID(menu_data['id']))
        assert menu is not None

        assert menu_data['title'] == menu.title
        assert menu_data['description'] == menu.description

    def test_create_menu_success(self, menu_service):
        response = client.post(
            reverse('create_menu'),
            json={
                'title': 'Menu 1',
                'description': 'Menu 1 description'
            }
        )
        assert response.status_code == 201
        menu_data = response.json()
        assert 'id' in menu_data

        menu = menu_service.get(UUID(menu_data['id']))
        assert menu is not None

        assert menu_data['title'] == menu.title == 'Menu 1'
        assert menu_data['description'] == menu.description == 'Menu 1 description'

    def test_update_menu_success(self, menu):
        response = client.patch(
            reverse('update_menu', menu_id=menu.id),
            json={
                'title': 'Updated Menu 1',
                'description': 'Updated Menu 1 description'
            }
        )
        assert response.status_code == 200
        menu_data = response.json()
        assert 'id' in menu_data
        assert menu_data['title'] == 'Updated Menu 1'
        assert menu_data['description'] == 'Updated Menu 1 description'

        response = client.get(
            reverse('read_menu', menu_id=menu.id)
        )
        assert response.status_code == 200
        menu_data = response.json()

        assert 'id' in menu_data
        assert menu_data['title'] == 'Updated Menu 1'
        assert menu_data['description'] == 'Updated Menu 1 description'

    def test_delete_menu_success(self, menu_service):
        menu_data = {
            'title': 'Menu 1',
            'description': 'Menu 1 description'
        }

        menu = menu_service.create(
            schemas.MenuCreate(**menu_data)
        )

        response = client.delete(
            reverse('delete_menu', menu_id=menu.id)
        )
        assert response.status_code == 200
        menu_data = response.json()
        assert 'id' in menu_data

        assert menu_data['title'] == menu.title
        assert menu_data['description'] == menu.description

        response = client.get(
            reverse('read_menu', menu_id=menu.id)
        )
        assert response.status_code == 404
