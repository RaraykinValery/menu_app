from uuid import UUID

from fastapi import Depends

from app.cache import DishCache, MenuCache, SubmenuCache
from app.custom_exceptions import EntityIsNotInCache
from app.repositories import DishRepository, MenuRepository, SubmenuRepository

from . import models, schemas


class MenuService:
    def __init__(
            self,
            cache: MenuCache = Depends(MenuCache),
            repository: MenuRepository = Depends(MenuRepository)
    ) -> None:
        self.cache = cache
        self.repository = repository

    def get_all(self) -> list[models.Menu]:
        try:
            db_menus = self.cache.get_list('menus_list')
        except EntityIsNotInCache:
            db_menus = self.repository.get_all()
            if db_menus:
                self.cache.save('menus_list', db_menus)

        return db_menus

    def get(self, menu_id: UUID) -> models.Menu:
        try:
            db_menu = self.cache.get(str(menu_id))
        except EntityIsNotInCache:
            db_menu = self.repository.get(menu_id)
            if db_menu:
                self.cache.save(str(menu_id), db_menu)

        return db_menu

    def create(self, menu: schemas.MenuCreate) -> models.Menu:
        self.cache.delete('menus_list')
        return self.repository.save(menu)

    def delete(self, menu_id: UUID) -> models.Menu:
        self.cache.delete_cascade(f'{menu_id}*')
        self.cache.delete('menus_list')
        return self.repository.delete(menu_id)

    def update(
            self,
            menu_id: UUID,
            menu: schemas.MenuUpdate
    ) -> models.Menu:
        self.cache.delete(str(menu_id))
        self.cache.delete('menus_list')
        return self.repository.update(menu_id, menu)


class SubmenuService:
    def __init__(
            self,
            cache: SubmenuCache = Depends(SubmenuCache),
            repository: SubmenuRepository = Depends(SubmenuRepository)
    ) -> None:
        self.cache = cache
        self.repository = repository

    def get_all(self, menu_id: UUID) -> list[models.Submenu]:
        try:
            db_submenus = self.cache.get_list(
                f'{menu_id}_submenus'
            )
        except EntityIsNotInCache:
            db_submenus = self.repository.get_all(menu_id)
            if db_submenus:
                self.cache.save(f'{menu_id}_submenus', db_submenus)

        return db_submenus

    def get(self, menu_id: UUID, submenu_id: UUID) -> models.Submenu:
        try:
            db_submenu = self.cache.get(
                f'{menu_id}_{submenu_id}'
            )
        except EntityIsNotInCache:
            db_submenu = self.repository.get(submenu_id)
            if db_submenu:
                self.cache.save(f'{menu_id}_{submenu_id}', db_submenu)

        return db_submenu

    def create(
            self,
            menu_id: UUID,
            submenu: schemas.SubmenuCreate
    ) -> models.Submenu:
        self.cache.delete(str(menu_id))
        self.cache.delete(f'{menu_id}_submenus')
        self.cache.delete('menus_list')
        return self.repository.save(menu_id, submenu)

    def delete(
            self,
            menu_id: UUID,
            submenu_id: UUID
    ) -> models.Submenu:
        self.cache.delete_cascade(f'{menu_id}_{submenu_id}*')
        self.cache.delete(f'{menu_id}_submenus')
        self.cache.delete(str(menu_id))
        return self.repository.delete(submenu_id)

    def update(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            submenu: schemas.SubmenuUpdate
    ) -> models.Submenu:
        self.cache.delete(f'{menu_id}_{submenu_id}')
        self.cache.delete(f'{menu_id}_submenus')
        self.cache.delete('menus_list')
        return self.repository.update(submenu_id, submenu)


class DishService:
    def __init__(
            self,
            cache: DishCache = Depends(DishCache),
            repository: DishRepository = Depends(DishRepository)
    ) -> None:
        self.cache = cache
        self.repository = repository

    def get_all(self, submenu_id: UUID) -> list[models.Dish]:
        try:
            db_dishes = self.cache.get_all(
                f'{submenu_id}_dishes'
            )
        except EntityIsNotInCache:
            db_dishes = self.repository.get_all(submenu_id)
            if db_dishes:
                self.cache.save(f'{submenu_id}_dishes', db_dishes)

        return db_dishes

    def get(self, menu_id, submenu_id, dish_id: UUID,) -> models.Dish:
        try:
            db_dish = self.cache.get(
                f'{menu_id}_{submenu_id}_{dish_id}'
            )
        except EntityIsNotInCache:
            db_dish = self.repository.get(dish_id)
            if db_dish:
                self.cache.save(f'{menu_id}_{submenu_id}_{dish_id}', db_dish)

        return db_dish

    def create(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish: schemas.DishCreate
    ) -> models.Dish:
        self.cache.delete(f'{menu_id}_{submenu_id}')
        self.cache.delete(f'{menu_id}')
        self.cache.delete('menus_list')
        self.cache.delete(f'{menu_id}_submenus')
        self.cache.delete(f'{submenu_id}_dishes')

        return self.repository.save(submenu_id, dish)

    def delete(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID
    ) -> models.Dish:
        self.cache.delete(f'{menu_id}_{submenu_id}_{dish_id}')
        self.cache.delete(f'{menu_id}_{submenu_id}')
        self.cache.delete(f'{menu_id}')
        self.cache.delete('menus_list')
        self.cache.delete(f'{menu_id}_submenus')
        self.cache.delete(f'{submenu_id}_dishes')

        return self.repository.delete(dish_id)

    def update(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish_id: UUID,
            dish: schemas.DishUpdate
    ) -> models.Dish:
        self.cache.delete(f'{menu_id}_{submenu_id}_{dish_id}')
        return self.repository.update(dish_id, dish)
