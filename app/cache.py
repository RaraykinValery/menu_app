import pickle

from fastapi import Depends

from app import schemas
from app.dependencies import get_cache_conn


class MenuCache:
    def __init__(self, cache=Depends(get_cache_conn)) -> None:
        self.cache = cache

    def get_list(self, key: str) -> list[schemas.MenuWithCounts] | None:
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def get(self, key: str) -> (schemas.MenuWithCounts | None):
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def save(
        self,
        key: str,
        value: schemas.MenuWithCounts | list[schemas.MenuWithCounts]
    ) -> None:
        self.cache.set(key, pickle.dumps(value))

    def delete_cascade(self, pattern: str):
        for key in self.cache.scan_iter(pattern):
            self.cache.delete(key)

    def delete(self, key: str):
        self.cache.delete(key)


class SubmenuCache:
    def __init__(self, cache=Depends(get_cache_conn)):
        self.cache = cache

    def get_list(self, key: str) -> list[schemas.Submenu] | None:
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def get(self, key: str) -> schemas.Submenu | None:
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def save(
        self,
        key: str,
        value: schemas.Submenu | list[schemas.Submenu]
    ) -> None:
        self.cache.set(key, pickle.dumps(value))

    def delete_cascade(self, pattern: str):
        for key in self.cache.scan_iter(pattern):
            self.cache.delete(key)

    def delete(self, key: str):
        self.cache.delete(key)


class DishCache:
    def __init__(self, cache=Depends(get_cache_conn)) -> None:
        self.cache = cache

    def get_all(
            self,
            key: str,
    ) -> list[schemas.Dish] | None:
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def get(
            self,
            key: str,
    ) -> schemas.Dish | None:
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def save(
        self,
        key: str,
        value: schemas.Dish | list[schemas.Dish]
    ) -> None:
        self.cache.set(key, pickle.dumps(value))

    def delete(
            self,
            key: str,
    ) -> None:
        self.cache.delete(key)
