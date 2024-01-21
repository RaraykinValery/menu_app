from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


def get_menus(db: Session):
    return db.query(models.Menu).all()


def get_menu(db: Session, menu_id: UUID):
    return db.get(models.Menu, menu_id)


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def delete_menu(db: Session, menu_id: UUID):
    db_menu = get_menu(db, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    db.delete(db_menu)
    db.commit()
    return db_menu


def update_menu(db: Session, menu_id: UUID, menu: schemas.MenuUpdate):
    db_menu = get_menu(db, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    menu_data = menu.model_dump(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(db_menu, key, value)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def get_submenus(db: Session, menu_id: UUID):
    submenus = db.query(models.Submenu).filter(
        models.Submenu.menu_id == menu_id).all()
    return submenus


def get_submenu(db: Session, submenu_id: UUID):
    return (db.query(models.Submenu)
            .filter(models.Submenu.id == submenu_id)
            .first())


def create_submenu(db: Session, menu_id: UUID, submenu: schemas.SubmenuCreate):
    db_menu = get_menu(db, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    db_submenu = models.Submenu(**submenu.model_dump())
    db_menu.submenus.append(db_submenu)
    db.commit()
    return db_submenu


def delete_submenu(db: Session, submenu_id: UUID):
    db_submenu = get_submenu(db, submenu_id)
    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    db.delete(db_submenu)
    db.commit()
    return db_submenu


def update_submenu(db: Session,
                   submenu_id: UUID,
                   submenu: schemas.SubmenuUpdate):
    db_submenu = get_submenu(db, submenu_id)
    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu_data = submenu.model_dump(exclude_unset=True)
    for key, value in submenu_data.items():
        setattr(db_submenu, key, value)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def get_dishes(db: Session, submenu_id: UUID):
    db_submenu = get_submenu(db, submenu_id)
    if not db_submenu:
        return []
    return db_submenu.dishes


def get_dish(db: Session, dish_id: UUID):
    return (db.query(models.Dish)
            .filter(models.Dish.id == dish_id)
            .first())


def create_dish(db: Session,
                submenu_id: UUID,
                dish: schemas.DishCreate):
    db_submenu = get_submenu(db, submenu_id)
    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    db_dish = models.Dish(**dish.model_dump())
    db_submenu.dishes.append(db_dish)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def delete_dish(db: Session, dish_id: UUID):
    db_dish = get_dish(db, dish_id)
    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    db.delete(db_dish)
    db.commit()
    return db_dish


def update_dish(db: Session,
                dish_id: UUID,
                dish: schemas.DishUpdate):
    db_dish = get_dish(db, dish_id)
    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    dish_data = dish.model_dump(exclude_unset=True)
    for key, value in dish_data.items():
        setattr(db_dish, key, value)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish
