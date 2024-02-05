from uuid import UUID

from fastapi import Depends

from app.cache import DishCache, MenuCache, SubmenuCache
from app.repositories import DishRepository, MenuRepository, SubmenuRepository

from . import schemas


class MenuService:
    def __init__(
            self,
            cache: MenuCache = Depends(MenuCache),
            repository: MenuRepository = Depends(MenuRepository)
    ) -> None:
        self.cache = cache
        self.repository = repository

    def get_all(self) -> list[schemas.MenuWithCounts]:
        menus = self.cache.get_list('menus_list')

        if not menus:
            menus = self.repository.get_all()
            if menus:
                self.cache.save('menus_list', menus)

        return menus

    def get(self, menu_id: UUID) -> schemas.MenuWithCounts | None:
        menu = self.cache.get(str(menu_id))

        if not menu:
            menu = self.repository.get(menu_id)
            if menu:
                self.cache.save(str(menu_id), menu)

        return menu

    def create(self, menu: schemas.MenuCreate) -> schemas.Menu:
        self.cache.delete('menus_list')
        return self.repository.save(menu)

    def delete(self, menu_id: UUID) -> schemas.Menu | None:
        self.cache.delete_cascade(f'{menu_id}*')
        self.cache.delete('menus_list')
        return self.repository.delete(menu_id)

    def update(
            self,
            menu_id: UUID,
            menu: schemas.MenuUpdate
    ) -> schemas.Menu | None:
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

    def get_all(self, menu_id: UUID) -> list[schemas.Submenu]:
        submenus = self.cache.get_list(f'{menu_id}_submenus')

        if not submenus:
            submenus = self.repository.get_all(menu_id)
            if submenus:
                self.cache.save(f'{menu_id}_submenus', submenus)

        return submenus

    def get(self, menu_id: UUID, submenu_id: UUID) -> schemas.Submenu | None:
        submenu = self.cache.get(f'{menu_id}_{submenu_id}')

        if not submenu:
            submenu = self.repository.get(submenu_id)
            if submenu:
                self.cache.save(f'{menu_id}_{submenu_id}', submenu)

        return submenu

    def create(
            self,
            menu_id: UUID,
            submenu: schemas.SubmenuCreate
    ) -> schemas.Submenu:
        self.cache.delete(str(menu_id))
        self.cache.delete(f'{menu_id}_submenus')
        self.cache.delete('menus_list')
        return self.repository.save(menu_id, submenu)

    def delete(
            self,
            menu_id: UUID,
            submenu_id: UUID
    ) -> schemas.Submenu | None:
        self.cache.delete_cascade(f'{menu_id}_{submenu_id}*')
        self.cache.delete(f'{menu_id}_submenus')
        self.cache.delete(str(menu_id))
        return self.repository.delete(submenu_id)

    def update(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            submenu: schemas.SubmenuUpdate
    ) -> schemas.Submenu | None:
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

    def get_all(self, submenu_id: UUID) -> list[schemas.Dish]:
        dishes = self.cache.get_all(f'{submenu_id}_dishes')

        if not dishes:
            dishes = self.repository.get_all(submenu_id)
            if dishes:
                self.cache.save(f'{submenu_id}_dishes', dishes)

        return dishes

    def get(self, menu_id, submenu_id, dish_id: UUID,) -> schemas.Dish | None:
        dish = self.cache.get(f'{menu_id}_{submenu_id}_{dish_id}')

        if not dish:
            dish = self.repository.get(dish_id)
            if dish:
                self.cache.save(f'{menu_id}_{submenu_id}_{dish_id}', dish)

        return dish

    def create(
            self,
            menu_id: UUID,
            submenu_id: UUID,
            dish: schemas.DishCreate
    ) -> schemas.Dish:
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
    ) -> schemas.Dish | None:
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
    ) -> schemas.Dish | None:
        self.cache.delete(f'{menu_id}_{submenu_id}_{dish_id}')
        return self.repository.update(dish_id, dish)
