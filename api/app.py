from fastapi import FastAPI
from api.controller import hello_controller, client_controller

app = FastAPI(title = "Sanyo")

app.include_router(hello_controller.router)
app.include_router(client_controller.router)