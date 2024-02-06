from uuid import UUID

from app import models, schemas, services
from app.utils import reverse
from tests.conftest import client


class TestDishRouts:
    def test_read_dishes_success(
            self,
            dish: models.Dish,
            dish_service: services.DishService
    ) -> None:
        response = client.get(
            reverse(
                'read_dishes',
                menu_id=dish.submenu.menu.id,
                submenu_id=dish.submenu_id
            ),
        )

        assert response.status_code == 200
        data = response.json()

        db_dishes = dish_service.get_all(dish.submenu_id)
        assert len(data) == len(db_dishes) == 1

    def test_read_dish_success(
            self,
            dish: models.Dish,
            dish_service: services.DishService
    ) -> None:
        response = client.get(
            reverse(
                'read_dish',
                menu_id=dish.submenu.menu.id,
                submenu_id=dish.submenu_id,
                dish_id=dish.id
            ),
        )
        assert response.status_code == 200
        dish_data = response.json()
        assert 'id' in dish_data

        db_dish = dish_service.get(
            dish.submenu.menu.id,
            dish.submenu.id,
            dish.id,
        )
        assert db_dish is not None

        assert dish_data['title'] == db_dish.title
        assert dish_data['description'] == db_dish.description
        assert dish_data['price'] == db_dish.price

    def test_create_dish_success(
            self,
            submenu: models.Submenu,
            dish_service: services.DishService
    ) -> None:
        response = client.post(
            reverse(
                'create_dish',
                menu_id=submenu.menu.id,
                submenu_id=submenu.id,
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

        db_dish = dish_service.get(
            submenu.menu.id,
            submenu.id,
            UUID(dish_data['id']),
        )
        assert db_dish is not None

        assert dish_data['title'] == db_dish.title
        assert dish_data['description'] == db_dish.description
        assert dish_data['price'] == db_dish.price

    def test_update_dish_success(
            self,
            dish: models.Dish
    ) -> None:
        response = client.patch(
            reverse(
                'update_dish',
                menu_id=dish.submenu.menu.id,
                submenu_id=dish.submenu_id,
                dish_id=dish.id
            ),
            json={
                'title': 'Updated Dish 1',
                'description': 'Updated Dish 1 description'
            }
        )
        assert response.status_code == 200
        dish_data = response.json()
        assert 'id' in dish_data
        assert dish_data['title'] == 'Updated Dish 1'
        assert dish_data['description'] == 'Updated Dish 1 description'

        response = client.get(
            reverse(
                'read_dish',
                menu_id=dish.submenu.menu.id,
                submenu_id=dish.submenu_id,
                dish_id=dish.id
            ),
        )
        assert response.status_code == 200
        dish_data = response.json()
        assert 'id' in dish_data
        assert dish_data['title'] == 'Updated Dish 1'
        assert dish_data['description'] == 'Updated Dish 1 description'

    def test_delete_dish_success(
            self,
            menu: models.Menu,
            submenu: models.Submenu,
            dish_service: services.DishService
    ) -> None:
        dish_data = {
            'title': 'Dish 1',
            'description': 'Dish 1 description',
            'price': '12.50'
        }

        dish = dish_service.create(
            menu.id,
            submenu.id,
            schemas.DishCreate(**dish_data)
        )

        response = client.delete(
            reverse(
                'delete_dish',
                menu_id=dish.submenu.menu.id,
                submenu_id=dish.submenu_id,
                dish_id=dish.id
            ),
        )
        assert response.status_code == 200
        dish_data = response.json()
        assert 'id' in dish_data

        assert dish_data['title'] == dish.title
        assert dish_data['description'] == dish.description
        assert dish_data['price'] == dish.price

        response = client.get(
            reverse(
                'read_dish',
                menu_id=dish.submenu.menu.id,
                submenu_id=dish.submenu_id,
                dish_id=dish.id
            )
        )
        assert response.status_code == 404
