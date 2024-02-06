from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app import models, schemas, services
from app.custom_exceptions import EntityDoesNotExist

router: APIRouter = APIRouter(
    prefix='/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['dishes']
)


@router.get(
    '/',
    response_model=list[schemas.Dish],
    tags=['get']
)
def read_dishes(
        submenu_id: UUID,
        service: services.DishService = Depends(services.DishService)
) -> list[models.Dish]:
    """Получить список блюд для указанного подменю"""
    return service.get_all(submenu_id)


@router.post(
    '/',
    response_model=schemas.Dish,
    status_code=status.HTTP_201_CREATED,
    tags=['post'],
    responses={
        404: {'description': 'Submenu not found'}
    }
)
def create_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish: schemas.DishCreate,
        service: services.DishService = Depends(services.DishService)
) -> models.Dish:
    """Создать новое блюдо для указанного подменю"""
    return service.create(menu_id, submenu_id, dish)


@router.get(
    '/{dish_id}',
    response_model=schemas.Dish,
    tags=['get'],
    responses={
        404: {'description': 'Dish not found'}
    }
)
def read_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        service: services.DishService = Depends(services.DishService)
) -> models.Dish:
    """Получить информацию о конкретном блюде для указанного подменю"""
    try:
        db_dish = service.get(menu_id, submenu_id, dish_id)
    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail='dish not found')

    return db_dish


@router.delete(
    '/{dish_id}',
    response_model=schemas.Dish,
    tags=['delete'],
    responses={
        404: {'description': 'Dish not found'}
    }

)
def delete_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        service: services.DishService = Depends(services.DishService)
) -> models.Dish:
    """Удалить блюдо для указанного подменю"""
    try:
        db_dish = service.delete(menu_id, submenu_id, dish_id)
    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail='dish not found')

    return db_dish


@router.patch(
    '/{dish_id}',
    response_model=schemas.Dish,
    tags=['patch'],
    responses={
        404: {'description': 'Dish not found'}
    }
)
def update_dish(
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        dish: schemas.DishUpdate,
        service: services.DishService = Depends(services.DishService)
) -> models.Dish:
    """Обновить информацию о блюде для указанного подменю"""
    try:
        db_dish = service.update(
            menu_id, submenu_id, dish_id, dish)
    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail='dish not found')

    return db_dish
