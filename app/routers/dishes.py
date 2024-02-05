from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app import schemas, services

router = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['dishes']
)


@router.get(
    '/',
    response_model=list[schemas.Dish]
)
def read_dishes(
        submenu_id: UUID,
        service: services.DishService = Depends(services.DishService)
) -> Any:
    return service.get_all(submenu_id)


@router.post(
    '/',
    response_model=schemas.Dish,
    status_code=status.HTTP_201_CREATED
)
def create_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish: schemas.DishCreate,
        service: services.DishService = Depends(services.DishService)
) -> Any:
    return service.create(menu_id, submenu_id, dish)


@router.get(
    '/{dish_id}',
    response_model=schemas.Dish
)
def read_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        service: services.DishService = Depends(services.DishService)
) -> Any:
    db_dish = service.get(menu_id, submenu_id, dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    return db_dish


@router.delete(
    '/{dish_id}',
    response_model=schemas.Dish
)
def delete_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        service: services.DishService = Depends(services.DishService)
) -> Any:
    return service.delete(menu_id, submenu_id, dish_id)


@router.patch(
    '/{dish_id}',
    response_model=schemas.Dish
)
def update_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish: schemas.DishUpdate,
        service: services.DishService = Depends(services.DishService)
) -> Any:
    return service.update(menu_id, submenu_id, dish_id, dish)
