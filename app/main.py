from fastapi import FastAPI

from . import models
from .database import engine
from .routers import api

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    api.router,
    prefix='/api/v1'
)
