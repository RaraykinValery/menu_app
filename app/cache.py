import pickle

from fastapi import Depends
from redis import Redis  # type: ignore

from app import models
from app.custom_exceptions import EntityIsNotInCache
from app.dependencies import get_cache_conn


class MenuCache:
    def __init__(self, cache: Redis = Depends(get_cache_conn)) -> None:
        self.cache = cache

    def get_list(self, key: str) -> list[models.Menu]:
        value = self.cache.get(key)

        if not value:
            raise EntityIsNotInCache

        return pickle.loads(value)

    def get(self, key: str) -> models.Menu:
        value = self.cache.get(key)

        if not value:
            raise EntityIsNotInCache

        return pickle.loads(value)

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
    def __init__(self, cache: Redis = Depends(get_cache_conn)) -> None:
        self.cache = cache

    def get_list(self, key: str) -> list[models.Submenu]:
        value = self.cache.get(key)

        if not value:
            raise EntityIsNotInCache

        return pickle.loads(value)

    def get(self, key: str) -> models.Submenu:
        value = self.cache.get(key)

        if not value:
            raise EntityIsNotInCache

        return pickle.loads(value)

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
    def __init__(self, cache: Redis = Depends(get_cache_conn)) -> None:
        self.cache = cache

    def get_all(
            self,
            key: str,
    ) -> list[models.Dish]:
        value = self.cache.get(key)

        if not value:
            raise EntityIsNotInCache

        return pickle.loads(value)

    def get(
            self,
            key: str,
    ) -> models.Dish:
        value = self.cache.get(key)

        if not value:
            raise EntityIsNotInCache

        return pickle.loads(value)

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
