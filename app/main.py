from fastapi import FastAPI

from api.endpoints import banner

app = FastAPI()

app.include_router(banner.router)
