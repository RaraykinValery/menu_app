from fastapi import APIRouter

from app.routers import dishes, menus, submenus

router = APIRouter()

router.include_router(menus.router)
router.include_router(submenus.router)
router.include_router(dishes.router)
