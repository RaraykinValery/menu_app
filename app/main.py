from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Menu routs


@app.get('/api/v1/menus', response_model=list[schemas.MenuWithCounts])
def read_menus(db: Session = Depends(get_db)):
    return crud.get_menus(db)


@app.get('/api/v1/menus/{menu_id}', response_model=schemas.MenuWithCounts)
def read_menu(menu_id: UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    return db_menu


@app.post('/api/v1/menus',
          response_model=schemas.Menu,
          status_code=status.HTTP_201_CREATED)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    return crud.create_menu(db, menu)


@app.delete('/api/v1/menus/{menu_id}', response_model=schemas.Menu)
def delete_menu(menu_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_menu(db, menu_id)


@app.patch('/api/v1/menus/{menu_id}', response_model=schemas.Menu)
def update_menu(menu_id: UUID,
                menu: schemas.MenuUpdate,
                db: Session = Depends(get_db)):
    return crud.update_menu(db, menu_id, menu)


# Submenu routs


@app.get('/api/v1/menus/{menu_id}/submenus',
         response_model=list[schemas.Submenu])
def read_submenus(menu_id: UUID, db: Session = Depends(get_db),):
    return crud.get_submenus(db, menu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
         response_model=schemas.Submenu)
def read_submenu(submenu_id: UUID,
                 db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    return db_submenu


@app.post('/api/v1/menus/{menu_id}/submenus',
          response_model=schemas.Submenu,
          status_code=status.HTTP_201_CREATED)
def create_submenu(menu_id: UUID,
                   submenu: schemas.SubmenuCreate,
                   db: Session = Depends(get_db)):
    return crud.create_submenu(db, menu_id, submenu)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
            response_model=schemas.Submenu)
def delete_submenu(submenu_id: UUID,
                   db: Session = Depends(get_db)):
    return crud.delete_submenu(db, submenu_id)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}',
           response_model=schemas.Submenu)
def update_submenu(submenu_id: UUID,
                   submenu: schemas.SubmenuUpdate,
                   db: Session = Depends(get_db)):
    return crud.update_submenu(db, submenu_id, submenu)


# Dish routs


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
         response_model=list[schemas.Dish])
def read_dishes(submenu_id: UUID,
                db: Session = Depends(get_db)):
    return crud.get_dishes(db, submenu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
         response_model=schemas.Dish)
def read_dish(dish_id: UUID,
              db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    return db_dish


@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
          response_model=schemas.Dish,
          status_code=status.HTTP_201_CREATED)
def create_dish(submenu_id: UUID,
                dish: schemas.DishCreate,
                db: Session = Depends(get_db)):
    return crud.create_dish(db, submenu_id, dish)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
            response_model=schemas.Dish)
def delete_dish(dish_id: UUID,
                db: Session = Depends(get_db)):
    return crud.delete_dish(db, dish_id)


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
           response_model=schemas.Dish)
def update_dish(dish_id: UUID,
                dish: schemas.DishUpdate,
                db: Session = Depends(get_db)):
    return crud.update_dish(db, dish_id, dish)
