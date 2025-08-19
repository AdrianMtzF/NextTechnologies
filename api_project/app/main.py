from fastapi import FastAPI
from app.routes import number_route

app = FastAPI()

app.include_router(number_route.router, prefix="/numbers", tags=["Numbers"])
