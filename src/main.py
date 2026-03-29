from fastapi import FastAPI

from src.core.config import settings


app = FastAPI(**settings.fastapi_kwargs)
