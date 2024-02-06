from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app import models, schemas, services
from app.custom_exceptions import EntityDoesNotExist

router = APIRouter(
    prefix='/menus/{menu_id}/submenus',
    tags=['submenus']
)


@router.get(
    '/',
    response_model=list[schemas.SubmenuWithCounts],
    tags=['get']
)
def read_submenus(
        menu_id: UUID,
        service: services.SubmenuService = Depends(services.SubmenuService)
) -> list[models.Submenu]:
    """Получить список подменю для указанного меню"""
    return service.get_all(menu_id)


@router.post(
    '/',
    response_model=schemas.Submenu,
    status_code=status.HTTP_201_CREATED,
    tags=['post'],
    responses={
        404: {'description': 'Menu not found'}
    }
)
def create_submenu(
        menu_id: UUID,
        submenu: schemas.SubmenuCreate,
        service: services.SubmenuService = Depends(services.SubmenuService)
) -> models.Submenu:
    """Создать новое подменю для указанного меню"""
    return service.create(menu_id, submenu)


@router.get(
    '/{submenu_id}',
    response_model=schemas.SubmenuWithCounts,
    tags=['get'],
    responses={
        404: {'description': 'Submenu not found'}
    }
)
def read_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        service: services.SubmenuService = Depends(services.SubmenuService)
) -> models.Submenu:
    """Получить информацию о конкретном подменю для указанного меню."""
    try:
        db_submenu = service.get(menu_id, submenu_id)
    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail='submenu not found')

    return db_submenu


@router.delete(
    '/{submenu_id}',
    response_model=schemas.Submenu,
    tags=['delete'],
    responses={
        404: {'description': 'Submenu not found'}
    }
)
def delete_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        service: services.SubmenuService = Depends(services.SubmenuService)
) -> models.Submenu:
    """Удалить подменю для указанного меню"""
    try:
        db_submenu = service.delete(menu_id, submenu_id)
    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail='submenu not found')

    return db_submenu


@router.patch(
    '/{submenu_id}',
    response_model=schemas.Submenu,
    tags=['patch'],
    responses={
        404: {'description': 'Submenu not found'}
    }
)
def update_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        submenu: schemas.SubmenuUpdate,
        service: services.SubmenuService = Depends(services.SubmenuService)
) -> models.Submenu:
    """Обновить информацию о подменю для указанного меню"""
    try:
        db_submenu = service.update(menu_id, submenu_id, submenu)
    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail='submenu not found')

    return db_submenu
