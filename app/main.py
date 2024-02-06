from fastapi import FastAPI

from . import api_description, models
from .database import engine
from .routers import api

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='MenuApp',
    openapi_tags=api_description.tags_metadata
)

app.include_router(
    api.router,
    prefix='/api/v1'
)
