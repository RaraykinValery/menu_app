from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.custom_exceptions import EntityDoesNotExist
from app.dependencies import get_db

from . import models, schemas


class MenuRepository:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session

    def get_all(self) -> list[models.Menu]:
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

        db_menus = []

        for res in db_results:
            db_menu, submenus_count, dishes_count = res
            db_menu.submenus_count = submenus_count
            db_menu.dishes_count = dishes_count
            db_menus.append(db_menu)

        return db_menus

    def get(self, id: UUID) -> models.Menu:
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

            return db_menu
        else:
            raise EntityDoesNotExist

    def save(self, menu: schemas.MenuCreate) -> models.Menu:
        db_menu = models.Menu(**menu.model_dump())
        self.session.add(db_menu)
        self.session.commit()
        self.session.refresh(db_menu)
        return db_menu

    def delete(self, id: UUID) -> models.Menu:
        db_menu = self.__get_by_id(id)
        if not db_menu:
            raise EntityDoesNotExist
        self.session.delete(db_menu)
        self.session.commit()
        return db_menu

    def update(
            self,
            id: UUID,
            element: schemas.MenuUpdate
    ) -> models.Menu:
        db_menu = self.__get_by_id(id)
        if not db_menu:
            raise EntityDoesNotExist
        menu_data = element.model_dump(exclude_unset=True)
        for key, value in menu_data.items():
            setattr(db_menu, key, value)
        self.session.add(db_menu)
        self.session.commit()
        self.session.refresh(db_menu)
        return db_menu

    def __get_by_id(self, id: UUID) -> models.Menu | None:
        return self.session.query(models.Menu).filter(
            models.Menu.id == id).first()


class SubmenuRepository:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session

    def get_all(self, menu_id: UUID) -> list[models.Submenu]:
        db_results = (
            self.session.query(
                models.Submenu,
                func.count(models.Dish.id).label('dish_count')
            )
            .outerjoin(models.Dish, models.Submenu.dishes)
            .outerjoin(models.Menu, models.Submenu.menu)
            .group_by(models.Submenu.id)
            .filter(models.Menu.id == menu_id)
            .all()
        )

        db_submenus = []

        for res in db_results:
            db_submenu, dishes_count = res
            db_submenu.dishes_count = dishes_count
            db_submenus.append(db_submenu)

        return db_submenus

    def get(self, submenu_id: UUID) -> models.Submenu:
        db_result = (
            self.session.query(
                models.Submenu,
                func.count(models.Dish.id).label('dish_count')
            )
            .outerjoin(models.Dish, models.Submenu.dishes)
            .group_by(models.Submenu.id)
            .filter(models.Submenu.id == submenu_id)
            .first()
        )

        if db_result:
            db_submenu, dishes_count = db_result
            db_submenu.dishes_count = dishes_count
            return db_submenu
        else:
            raise EntityDoesNotExist

    def save(
            self,
            menu_id: UUID,
            submenu: schemas.SubmenuCreate
    ) -> models.Submenu:
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
        return db_submenu

    def delete(
            self,
            id: UUID
    ) -> models.Submenu:
        db_submenu = self.__get_by_id(id)
        if not db_submenu:
            raise EntityDoesNotExist
        self.session.delete(db_submenu)
        self.session.commit()
        return db_submenu

    def update(
            self,
            id: UUID,
            submenu: schemas.SubmenuUpdate
    ) -> models.Submenu:
        db_submenu = self.__get_by_id(id)
        if not db_submenu:
            raise EntityDoesNotExist
        submenu_data = submenu.model_dump(exclude_unset=True)
        for key, value in submenu_data.items():
            setattr(db_submenu, key, value)
        self.session.add(db_submenu)
        self.session.commit()
        self.session.refresh(db_submenu)
        return db_submenu

    def __get_by_id(self, id: UUID) -> models.Submenu | None:
        return (
            self.session.query(models.Submenu)
            .filter(models.Submenu.id == id)
            .first()
        )


class DishRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_all(self, submenu_id: UUID) -> list[models.Dish]:
        db_dishes = (
            self.session.query(models.Dish)
            .filter(models.Dish.submenu_id == submenu_id)
            .all()
        )

        return db_dishes

    def get(self, id: UUID) -> models.Dish:
        db_dish = self.__get_by_id(id)

        if not db_dish:
            raise EntityDoesNotExist

        return db_dish

    def save(
            self,
            submenu_id: UUID,
            dish: schemas.DishCreate
    ) -> models.Dish:
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
        return db_dish

    def delete(self, id: UUID) -> models.Dish:
        db_dish = self.__get_by_id(id)
        if not db_dish:
            raise EntityDoesNotExist
        self.session.delete(db_dish)
        self.session.commit()
        return db_dish

    def update(
            self,
            id: UUID,
            dish: schemas.DishUpdate
    ) -> models.Dish:
        db_dish = self.__get_by_id(id)
        if not db_dish:
            raise EntityDoesNotExist
        dish_data = dish.model_dump(exclude_unset=True)
        for key, value in dish_data.items():
            setattr(db_dish, key, value)
        self.session.add(db_dish)
        self.session.commit()
        self.session.refresh(db_dish)
        return db_dish

    def __get_by_id(self, id: UUID) -> models.Dish | None:
        return (
            self.session.query(models.Dish)
            .filter(models.Dish.id == id)
            .first()
        )
