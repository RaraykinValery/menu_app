from starlette.datastructures import URLPath

from app.main import app


def reverse(name: str, *args, **kwargs) -> URLPath:
    return app.url_path_for(name, *args, **kwargs)
