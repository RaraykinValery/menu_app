import pytest
from fastapi.testclient import TestClient

from app import cache, models, repositories, schemas, services
from app.database import SessionLocal, engine
from app.dependencies import get_cache_conn
from app.main import app

client = TestClient(app)


def base_session():
    models.Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()

    yield db_session

    db_session.close()
    models.Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='class')
def class_session():
    yield from base_session()


@pytest.fixture()
def session():
    yield from base_session()


@pytest.fixture()
def cache_conn():
    cache_conn = get_cache_conn()

    yield cache_conn

    cache_conn.close


@pytest.fixture()
def menu_repository(session):
    return repositories.MenuRepository(session)


@pytest.fixture()
def menu_cache(cache_conn):
    return cache.MenuCache(cache_conn)


@pytest.fixture()
def menu_service(menu_cache, menu_repository):
    return services.MenuService(menu_cache, menu_repository)


@pytest.fixture()
def submenu_repository(session):
    return repositories.SubmenuRepository(session)


@pytest.fixture()
def submenu_cache(cache_conn):
    return cache.SubmenuCache(cache_conn)


@pytest.fixture()
def submenu_service(submenu_cache, submenu_repository):
    return services.SubmenuService(submenu_cache, submenu_repository)


@pytest.fixture()
def dish_repository(session):
    return repositories.DishRepository(session)


@pytest.fixture()
def dish_cache(cache_conn):
    return cache.DishCache(cache_conn)


@pytest.fixture()
def dish_service(dish_cache, dish_repository):
    return services.DishService(dish_cache, dish_repository)


@pytest.fixture
def menu(menu_repository):
    menu_data = {
        'title': 'Menu 1',
        'description': 'Menu 1 description'
    }

    db_menu = menu_repository.save(
        schemas.MenuCreate(**menu_data)
    )
    yield db_menu

    menu_repository.delete(db_menu.id)


@pytest.fixture
def submenu(menu, submenu_repository):
    submenu_data = {
        'title': 'Submenu 1',
        'description': 'Submenu 1 description'
    }

    db_submenu = submenu_repository.save(
        menu.id,
        schemas.SubmenuCreate(**submenu_data)
    )
    yield db_submenu

    submenu_repository.delete(db_submenu.id)


@pytest.fixture
def dish(submenu, dish_repository):
    dish_data = {
        'title': 'Dish 1',
        'description': 'Dish 1 description',
        'price': '12.50'
    }

    db_dish = dish_repository.save(
        submenu.id,
        schemas.DishCreate(**dish_data)
    )
    yield db_dish

    dish_repository.delete(db_dish.id)
