from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models


def get_menus_with_submenus_and_dishes_counts(session: Session, menu_id: UUID):
    return (
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
