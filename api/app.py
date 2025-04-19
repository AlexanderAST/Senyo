from fastapi import FastAPI
from api.controller import hello_controller, client_controller, address_controller, referrals_controller, promotions_controller, make_appointment_controller, service_controller, place_type_controller

app = FastAPI(title = "Sanyo")

app.include_router(hello_controller.router)
app.include_router(client_controller.router)
app.include_router(address_controller.router)
app.include_router(referrals_controller.router)
app.include_router(promotions_controller.router)
app.include_router(make_appointment_controller.router)
app.include_router(service_controller.router)
app.include_router(place_type_controller.router)