from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app import models, schemas, services
from app.custom_exceptions import EntityDoesNotExist

router = APIRouter(
    prefix='/menus',
    tags=['menus']
)


@router.get(
    '/',
    response_model=list[schemas.MenuWithCounts],
    tags=['get'],
)
def read_menus(
        service: services.MenuService = Depends(services.MenuService)
) -> list[models.Menu]:
    """Получить список меню"""
    return service.get_all()


@router.post(
    '/',
    response_model=schemas.Menu,
    status_code=status.HTTP_201_CREATED,
    tags=['post']
)
def create_menu(
    menu: schemas.MenuCreate,
    service: services.MenuService = Depends(services.MenuService)
) -> models.Menu:
    """Создать новое меню"""
    return service.create(menu)


@router.get(
    '/{menu_id}',
    response_model=schemas.MenuWithCounts,
    tags=['get'],
    responses={
        404: {'description': 'Menu not found'}
    }
)
def read_menu(
    menu_id: UUID,
    service: services.MenuService = Depends(services.MenuService)
) -> models.Menu:
    """Получить информацию о конкретном меню"""
    try:
        db_menu = service.get(menu_id)
    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail='menu not found')

    return db_menu


@router.delete(
    '/{menu_id}',
    response_model=schemas.Menu,
    tags=['delete'],
    responses={
        404: {'description': 'Menu not found'}
    }
)
def delete_menu(
    menu_id: UUID,
    service: services.MenuService = Depends(services.MenuService)
) -> models.Menu:
    """Удалить меню"""
    try:
        db_menu = service.delete(menu_id)
    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail='menu not found')

    return db_menu


@router.patch(
    '/{menu_id}',
    response_model=schemas.Menu,
    tags=['patch'],
    responses={
        404: {'description': 'Menu not found'}
    }
)
def update_menu(
    menu_id: UUID,
    menu: schemas.MenuUpdate,
    service: services.MenuService = Depends(services.MenuService)
) -> models.Menu:
    """Обновить информацию о меню"""
    try:
        db_menu = service.update(menu_id, menu)
    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail='menu not found')

    return db_menu
