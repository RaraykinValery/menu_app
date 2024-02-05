from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies import get_db

from . import models, schemas


def serialize(db_model, schema):
    return schema.model_validate(db_model)


class MenuRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_all(self) -> list[schemas.MenuWithCounts]:
        db_results = (
            self.session.query(
                models.Menu,
                func.count(func.distinct(models.Submenu.id)
                           ).label('submenus_count'),
                func.count(func.distinct(models.Dish.id)).label('dishes_count')
            )
            .outerjoin(
                models.Submenu,
                models.Submenu.menu_id == models.Menu.id
            )
            .outerjoin(
                models.Dish,
                models.Submenu.id == models.Dish.submenu_id
            )
            .group_by(models.Menu.id)
            .all()
        )

        menus = []

        for res in db_results:
            db_menu, submenus_count, dishes_count = res
            db_menu.submenus_count = submenus_count
            db_menu.dishes_count = dishes_count
            menu = serialize(db_menu, schemas.MenuWithCounts)
            menus.append(menu)

        return menus

    def get(self, id: UUID) -> schemas.MenuWithCounts | None:
        db_result = (
            self.session.query(
                models.Menu,
                func.count(func.distinct(models.Submenu.id)
                           ).label('submenus_count'),
                func.count(func.distinct(models.Dish.id)).label('dishes_count')
            )
            .outerjoin(
                models.Submenu,
                models.Submenu.menu_id == models.Menu.id
            )
            .outerjoin(
                models.Dish,
                models.Submenu.id == models.Dish.submenu_id
            )
            .filter(models.Menu.id == id)
            .group_by(models.Menu.id)
            .first()
        )

        if db_result:
            db_menu, submenus_count, dishes_count = db_result
            db_menu.submenus_count = submenus_count
            db_menu.dishes_count = dishes_count

            return serialize(db_menu, schemas.MenuWithCounts)

        return None

    def save(self, menu: schemas.MenuCreate) -> schemas.Menu:
        db_menu = models.Menu(**menu.model_dump())
        self.session.add(db_menu)
        self.session.commit()
        self.session.refresh(db_menu)
        return serialize(db_menu, schemas.Menu)

    def delete(self, id: UUID) -> schemas.Menu | None:
        db_menu = self.__get_by_id(id)
        if not db_menu:
            return None
        self.session.delete(db_menu)
        self.session.commit()
        return serialize(db_menu, schemas.Menu)

    def update(
            self,
            id: UUID,
            element: schemas.MenuUpdate
    ) -> schemas.Menu | None:
        db_menu = self.__get_by_id(id)
        if not db_menu:
            return None
        menu_data = element.model_dump(exclude_unset=True)
        for key, value in menu_data.items():
            setattr(db_menu, key, value)
        self.session.add(db_menu)
        self.session.commit()
        self.session.refresh(db_menu)
        return serialize(db_menu, schemas.Menu)

    def __get_by_id(self, id: UUID):
        return self.session.query(models.Menu).filter(
            models.Menu.id == id).first()


class SubmenuRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_all(self, menu_id: UUID) -> list[schemas.Submenu]:
        db_submenus = (self.session.query(models.Submenu)
                       .filter(models.Submenu.menu_id == menu_id)
                       .all()
                       )
        submenus = []

        if db_submenus:
            submenus = ([
                serialize(db_submenu, schemas.Submenu)
                for db_submenu
                in db_submenus
            ])

        return submenus

    def get(self, id: UUID) -> schemas.Submenu | None:
        db_submenu = self.__get_by_id(id)

        if db_submenu:
            return serialize(db_submenu, schemas.Submenu)

        return None

    def save(
            self,
            menu_id: UUID,
            submenu: schemas.SubmenuCreate
    ) -> schemas.Submenu:
        db_menu = (
            self.session.query(models.Menu)
            .filter(models.Menu.id == menu_id)
            .first()
        )
        if not db_menu:
            raise HTTPException(status_code=404, detail='menu not found')
        db_submenu = models.Submenu(**submenu.model_dump())
        db_menu.submenus.append(db_submenu)
        self.session.commit()
        return serialize(db_submenu, schemas.Submenu)

    def delete(
            self,
            id: UUID
    ) -> schemas.Submenu | None:
        db_submenu = self.__get_by_id(id)
        if not db_submenu:
            raise HTTPException(status_code=404, detail='submenu not found')
        self.session.delete(db_submenu)
        self.session.commit()
        return serialize(db_submenu, schemas.Submenu)

    def update(
            self,
            id: UUID,
            submenu: schemas.SubmenuUpdate
    ) -> schemas.Submenu | None:
        db_submenu = self.__get_by_id(id)
        if not db_submenu:
            raise HTTPException(status_code=404, detail='submenu not found')
        submenu_data = submenu.model_dump(exclude_unset=True)
        for key, value in submenu_data.items():
            setattr(db_submenu, key, value)
        self.session.add(db_submenu)
        self.session.commit()
        self.session.refresh(db_submenu)
        return serialize(db_submenu, schemas.Submenu)

    def __get_by_id(self, id: UUID):
        return (
            self.session.query(models.Submenu)
            .filter(models.Submenu.id == id)
            .first()
        )


class DishRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_all(self, submenu_id: UUID) -> list[schemas.Dish]:
        db_dishes = (
            self.session.query(models.Dish)
            .filter(models.Dish.submenu_id == submenu_id)
            .all()
        )

        dishes = []

        if db_dishes:
            dishes = ([
                serialize(db_dish, schemas.Dish)
                for db_dish
                in db_dishes
            ])

        return dishes

    def get(self, id: UUID) -> schemas.Dish | None:
        db_dish = self.__get_by_id(id)

        if db_dish:
            return serialize(db_dish, schemas.Dish)

        return None

    def save(
            self,
            submenu_id: UUID,
            dish: schemas.DishCreate
    ) -> schemas.Dish:
        db_submenu = (
            self.session.query(models.Submenu)
            .filter(models.Submenu.id == submenu_id)
            .first()
        )
        if not db_submenu:
            raise HTTPException(status_code=404, detail='submenu not found')
        db_dish = models.Dish(**dish.model_dump())
        db_submenu.dishes.append(db_dish)
        self.session.add(db_dish)
        self.session.commit()
        self.session.refresh(db_dish)
        return serialize(db_dish, schemas.Dish)

    def delete(self, id: UUID) -> schemas.Dish | None:
        db_dish = self.__get_by_id(id)
        if not db_dish:
            raise HTTPException(status_code=404, detail='dish not found')
        self.session.delete(db_dish)
        self.session.commit()
        return serialize(db_dish, schemas.Dish)

    def update(
            self,
            id: UUID,
            dish: schemas.DishUpdate
    ) -> schemas.Dish | None:
        db_dish = self.__get_by_id(id)
        if not db_dish:
            raise HTTPException(status_code=404, detail='dish not found')
        dish_data = dish.model_dump(exclude_unset=True)
        for key, value in dish_data.items():
            setattr(db_dish, key, value)
        self.session.add(db_dish)
        self.session.commit()
        self.session.refresh(db_dish)
        return serialize(db_dish, schemas.Dish)

    def __get_by_id(self, id: UUID):
        return (
            self.session.query(models.Dish)
            .filter(models.Dish.id == id)
            .first()
        )
