from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app import schemas, services

router = APIRouter(
    prefix='/menus',
    tags=['menus']
)


@router.get('/', response_model=list[schemas.MenuWithCounts])
def read_menus(
        service: services.MenuService = Depends(services.MenuService)
) -> Any:
    return service.get_all()


@router.post('/',
             response_model=schemas.Menu,
             status_code=status.HTTP_201_CREATED)
def create_menu(
    menu: schemas.MenuCreate,
    service: services.MenuService = Depends(services.MenuService)
) -> Any:
    return service.create(menu)


@router.get('/{menu_id}', response_model=schemas.MenuWithCounts)
def read_menu(
    menu_id: UUID,
    service: services.MenuService = Depends(services.MenuService)
) -> Any:
    db_menu = service.get(menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    return db_menu


@router.delete('/{menu_id}', response_model=schemas.Menu)
def delete_menu(
    menu_id: UUID,
    service: services.MenuService = Depends(services.MenuService)
) -> Any:
    db_menu = service.delete(menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    return db_menu


@router.patch('/{menu_id}', response_model=schemas.Menu)
def update_menu(
    menu_id: UUID,
    menu: schemas.MenuUpdate,
    service: services.MenuService = Depends(services.MenuService)
) -> Any:
    db_menu = service.update(menu_id, menu)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    return db_menu
