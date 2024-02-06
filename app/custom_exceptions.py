class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""


class EntityIsNotInCache(Exception):
    """Raised when entity was not found in cache."""
