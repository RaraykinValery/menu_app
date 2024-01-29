from uuid import UUID

from sqlalchemy.orm import Session

from tests.conftest import client
from app import operations


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
    menu_with_counts = operations.get_menu_with_submenus_and_dishes_counts(
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
