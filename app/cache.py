import pickle

from fastapi import Depends

from app import models
from app.dependencies import get_cache_conn


class MenuCache:
    def __init__(self, cache=Depends(get_cache_conn)) -> None:
        self.cache = cache

    def get_list(self, key: str) -> list[models.Menu] | None:
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def get(self, key: str) -> (models.Menu | None):
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def save(
        self,
        key: str,
        value: models.Menu | list[models.Menu]
    ) -> None:
        self.cache.set(key, pickle.dumps(value))

    def delete_cascade(self, pattern: str) -> None:
        for key in self.cache.scan_iter(pattern):
            self.cache.delete(key)

    def delete(self, key: str) -> None:
        self.cache.delete(key)


class SubmenuCache:
    def __init__(self, cache=Depends(get_cache_conn)) -> None:
        self.cache = cache

    def get_list(self, key: str) -> list[models.Submenu] | None:
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def get(self, key: str) -> models.Submenu | None:
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def save(
        self,
        key: str,
        value: models.Submenu | list[models.Submenu]
    ) -> None:
        self.cache.set(key, pickle.dumps(value))

    def delete_cascade(self, pattern: str) -> None:
        for key in self.cache.scan_iter(pattern):
            self.cache.delete(key)

    def delete(self, key: str) -> None:
        self.cache.delete(key)


class DishCache:
    def __init__(self, cache=Depends(get_cache_conn)) -> None:
        self.cache = cache

    def get_all(
            self,
            key: str,
    ) -> list[models.Dish] | None:
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def get(
            self,
            key: str,
    ) -> models.Dish | None:
        value = self.cache.get(key)
        if value:
            return pickle.loads(value)
        else:
            return None

    def save(
        self,
        key: str,
        value: models.Dish | list[models.Dish]
    ) -> None:
        self.cache.set(key, pickle.dumps(value))

    def delete(
            self,
            key: str,
    ) -> None:
        self.cache.delete(key)
