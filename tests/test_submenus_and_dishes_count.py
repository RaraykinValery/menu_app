from uuid import UUID

from sqlalchemy.orm import Session

from app import repositories
from app.utils import reverse
from tests.conftest import client


class TestSubmenusAndDishesCounts:
    menu_id = ''
    submenu_id = ''

    def test_create_menu_success(self, class_session: Session):
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

        TestSubmenusAndDishesCounts.menu_id = menu_data['id']

    def test_create_submenu_success(self, class_session: Session):
        response = client.post(
            reverse(
                'create_submenu',
                menu_id=TestSubmenusAndDishesCounts.menu_id
            ),
            json={
                'title': 'Submenu 1',
                'description': 'Submenu 1 description'
            }
        )
        assert response.status_code == 201
        submenu_data = response.json()
        assert 'id' in submenu_data

        TestSubmenusAndDishesCounts.submenu_id = submenu_data['id']

    def test_create_dish_1_success(self, class_session: Session):
        response = client.post(
            reverse(
                'create_dish',
                menu_id=TestSubmenusAndDishesCounts.menu_id,
                submenu_id=TestSubmenusAndDishesCounts.submenu_id
            ),
            json={
                'title': 'Dish 1',
                'description': 'Dish 1 description',
                'price': '15.47'
            }
        )
        assert response.status_code == 201
        dish_data = response.json()
        assert 'id' in dish_data

    def test_create_dish_2_success(self, class_session: Session):
        response = client.post(
            reverse(
                'create_dish',
                menu_id=TestSubmenusAndDishesCounts.menu_id,
                submenu_id=TestSubmenusAndDishesCounts.submenu_id
            ),
            json={
                'title': 'Dish 2',
                'description': 'Dish 2 description',
                'price': '20.45'
            }
        )
        assert response.status_code == 201
        dish_data = response.json()
        assert 'id' in dish_data

    def test_read_menu_success(self, class_session: Session):
        response = client.get(
            reverse('read_menu', menu_id=TestSubmenusAndDishesCounts.menu_id)
        )
        assert response.status_code == 200
        menu_data = response.json()
        assert menu_data['id'] == TestSubmenusAndDishesCounts.menu_id
        menu_repository = repositories.MenuRepository(class_session)
        menu_with_counts = menu_repository.get(UUID(menu_data['id']))
        assert menu_with_counts is not None
        assert menu_data['submenus_count'] == menu_with_counts.submenus_count
        assert menu_data['dishes_count'] == menu_with_counts.dishes_count

    def test_read_submenu(self, class_session: Session):
        response = client.get(
            reverse(
                'read_submenu',
                menu_id=TestSubmenusAndDishesCounts.menu_id,
                submenu_id=TestSubmenusAndDishesCounts.submenu_id
            )
        )
        assert response.status_code == 200
        submenu_data = response.json()
        assert submenu_data['id'] == TestSubmenusAndDishesCounts.submenu_id
        assert submenu_data['dishes_count'] == 2

    def test_delete_submenu_success(self, class_session: Session):
        response = client.delete(
            reverse(
                'delete_submenu',
                menu_id=TestSubmenusAndDishesCounts.menu_id,
                submenu_id=TestSubmenusAndDishesCounts.submenu_id
            )

        )
        assert response.status_code == 200

    def test_read_submenus_success(self, class_session: Session):
        response = client.get(
            reverse('read_submenus', menu_id=TestSubmenusAndDishesCounts.menu_id)
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_read_dishes(self, class_session: Session):
        response = client.get(
            reverse(
                'read_dishes',
                menu_id=TestSubmenusAndDishesCounts.menu_id,
                submenu_id=TestSubmenusAndDishesCounts.submenu_id
            )
        )
        assert response.status_code == 200
        assert response.json() == []

    def test_read_menu_with_no_submenus_and_dishes_success(
            self,
            class_session: Session
    ):
        response = client.get(
            reverse(
                'read_menu',
                menu_id=TestSubmenusAndDishesCounts.menu_id,
            )
        )
        assert response.status_code == 200
        menu_read_data = response.json()
        assert menu_read_data['id'] == TestSubmenusAndDishesCounts.menu_id
        assert menu_read_data['submenus_count'] == 0
        assert menu_read_data['dishes_count'] == 0

    def test_delete_menu_success(self, class_session: Session):
        response = client.delete(
            reverse('delete_menu', menu_id=TestSubmenusAndDishesCounts.menu_id)
        )
        assert response.status_code == 200

    def test_read_menus(self, class_session: Session):
        response = client.get(reverse('read_menus'))
        assert response.status_code == 200
        assert response.json() == []
