from pydantic import UUID4, BaseModel, ConfigDict


class DishBase(BaseModel):
    title: str
    description: str
    price: str


class DishCreate(DishBase):
    pass


class DishUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class Dish(DishBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    submenu_id: UUID4


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class Submenu(SubmenuBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    menu_id: UUID4
    dishes_count: int


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class Menu(MenuBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    submenus_count: int
    dishes_count: int
