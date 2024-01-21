from pydantic import UUID4, BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    pass


class DishUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class Dish(DishBase):
    id: UUID4
    submenu_id: UUID4

    class Config:
        from_attributes = True


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class Submenu(SubmenuBase):
    id: UUID4
    menu_id: UUID4
    dishes: list[Dish] = []

    class Config:
        from_attributes = True


class SubmenuAsListItem(Submenu):
    dish_count: int


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class Menu(MenuBase):
    id: UUID4
    submenus: list[Submenu] = []

    class Config:
        from_attributes = True


class MenuAsListItem(Menu):
    submenu_count: int
    dish_count: int
