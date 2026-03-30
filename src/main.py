from fastapi import FastAPI

from src import models  # noqa
from src.core.config import settings
from src.api.v1.router import v1_router


app = FastAPI(**settings.fastapi_kwargs)

app.include_router(v1_router)
