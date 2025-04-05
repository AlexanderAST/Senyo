from fastapi import FastAPI
from api.controller import hello_controller

app = FastAPI()

app.include_router(hello_controller.router)