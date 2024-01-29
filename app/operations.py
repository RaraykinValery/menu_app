from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models


def get_menu_with_submenus_and_dishes_counts(session: Session, menu_id: UUID):
    db_result = (
        session.query(
            models.Menu,
            func.count(func.distinct(models.Submenu.id)
                       ).label('submenus_count'),
            func.count(func.distinct(models.Dish.id)).label('dishes_count')
        )
        .outerjoin(models.Submenu, models.Submenu.menu_id == models.Menu.id)
        .outerjoin(models.Dish, models.Submenu.id == models.Dish.submenu_id)
        .filter(models.Menu.id == menu_id)
        .group_by(models.Menu.id)
        .first()
    )

    if db_result:
        menu, submenus_count, dishes_count = db_result
        menu.submenus_count = submenus_count
        menu.dishes_count = dishes_count

        return menu
    else:
        return None


def get_all_menus_with_submenus_and_dishes_counts(session: Session):
    db_results = (
        session.query(
            models.Menu,
            func.count(func.distinct(models.Submenu.id)
                       ).label('submenus_count'),
            func.count(func.distinct(models.Dish.id)).label('dishes_count')
        )
        .outerjoin(models.Submenu, models.Submenu.menu_id == models.Menu.id)
        .outerjoin(models.Dish, models.Submenu.id == models.Dish.submenu_id)
        .group_by(models.Menu.id)
        .all()
    )

    menus = []

    for res in db_results:
        menu, submenus_count, dishes_count = res
        menu.submenus_count = submenus_count
        menu.dishes_count = dishes_count
        menus.append(menu)

    return menus
