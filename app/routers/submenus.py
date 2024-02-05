from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app import schemas, services

router = APIRouter(
    prefix='/menus/{menu_id}/submenus',
    tags=['submenus']
)


@router.get(
    '/',
    response_model=list[schemas.Submenu]
)
def read_submenus(
        menu_id: UUID,
        service: services.SubmenuService = Depends(services.SubmenuService)
) -> Any:
    return service.get_all(menu_id)


@router.post(
    '/',
    response_model=schemas.Submenu,
    status_code=status.HTTP_201_CREATED
)
def create_submenu(
        menu_id: UUID,
        submenu: schemas.SubmenuCreate,
        service: services.SubmenuService = Depends(services.SubmenuService)
) -> Any:
    return service.create(menu_id, submenu)


@router.get(
    '/{submenu_id}',
    response_model=schemas.Submenu
)
def read_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        service: services.SubmenuService = Depends(services.SubmenuService)
) -> Any:
    db_submenu = service.get(menu_id, submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    return db_submenu


@router.delete(
    '/{submenu_id}',
    response_model=schemas.Submenu
)
def delete_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        service: services.SubmenuService = Depends(services.SubmenuService)
) -> Any:
    return service.delete(menu_id, submenu_id)


@router.patch(
    '/{submenu_id}',
    response_model=schemas.Submenu
)
def update_submenu(
        menu_id: UUID,
        submenu_id: UUID,
        submenu: schemas.SubmenuUpdate,
        service: services.SubmenuService = Depends(services.SubmenuService)
) -> Any:
    return service.update(menu_id, submenu_id, submenu)
