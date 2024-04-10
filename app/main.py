from fastapi import FastAPI

from app.api.endpoints import banner

app = FastAPI()

app.include_router(banner.router)
