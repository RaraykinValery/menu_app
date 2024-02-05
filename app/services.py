from uuid import UUID

from fastapi import Depends

from app.dependencies import get_repository
from app.repositories import DishRepository, MenuRepository, SubmenuRepository

from . import models, schemas


class MenuService:
    def __init__(
            self,
            repository: MenuRepository = Depends(
                get_repository(MenuRepository)
            )
    ) -> None:
        self.repository = repository

    def get_all(self) -> list[models.Menu]:
        return self.repository.get_all()

    def get(self, id: UUID) -> models.Menu | None:
        return self.repository.get(id)

    def create(self, menu: schemas.MenuCreate) -> models.Menu:
        return self.repository.save(menu)

    def delete(self, id: UUID) -> models.Menu | None:
        return self.repository.delete(id)

    def update(self, id: UUID, menu: schemas.MenuUpdate) -> models.Menu | None:
        return self.repository.update(id, menu)


class SubmenuService:
    def __init__(
            self,
            repository: SubmenuRepository = Depends(
                get_repository(SubmenuRepository)
            )
    ) -> None:
        self.repository = repository

    def get_all(self, menu_id: UUID) -> list[models.Submenu]:
        return self.repository.get_all(menu_id)

    def get(self, id: UUID,) -> models.Submenu | None:
        return self.repository.get(id)

    def create(
            self,
            menu_id: UUID,
            submenu: schemas.SubmenuCreate
    ) -> models.Submenu:
        return self.repository.save(menu_id, submenu)

    def delete(self, id: UUID) -> models.Submenu | None:
        return self.repository.delete(id)

    def update(
            self,
            id: UUID,
            submenu: schemas.SubmenuUpdate
    ) -> models.Submenu | None:
        return self.repository.update(id, submenu)


class DishService:
    def __init__(
            self,
            repository: DishRepository = Depends(
                get_repository(DishRepository)
            )
    ) -> None:
        self.repository = repository

    def get_all(self, submenu_id: UUID) -> list[models.Dish]:
        return self.repository.get_all(submenu_id)

    def get(self, id: UUID,) -> models.Dish | None:
        return self.repository.get(id)

    def create(
            self,
            submenu_id: UUID,
            dish: schemas.DishCreate
    ) -> models.Dish:
        return self.repository.save(submenu_id, dish)

    def delete(self, id: UUID) -> models.Dish | None:
        return self.repository.delete(id)

    def update(
            self,
            id: UUID,
            dish: schemas.DishUpdate
    ) -> models.Dish | None:
        return self.repository.update(id, dish)
