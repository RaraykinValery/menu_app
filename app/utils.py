from app.main import app


def reverse(name: str, *args, **kwargs):
    return app.url_path_for(name, *args, **kwargs)
