from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.service.promotions_service import PromotionsService
from fastapi import FastAPI
from api.controller import hello_controller, client_controller, address_controller, point_logs_controller, referrals_controller, promotions_controller, make_appointment_controller, service_controller, place_type_controller
from api.database import engine, AsyncSessionLocal  # Импорт из database.py

app = FastAPI(title = "Sanyo")

app.include_router(hello_controller.router)
app.include_router(client_controller.router)
app.include_router(address_controller.router)
app.include_router(referrals_controller.router)
app.include_router(promotions_controller.router)
app.include_router(make_appointment_controller.router)
app.include_router(service_controller.router)
app.include_router(place_type_controller.router)
app.include_router(point_logs_controller.router)

promotions_service = PromotionsService()

scheduler = AsyncIOScheduler()

async def daily_promo_task():
    async with AsyncSessionLocal() as db:  # Используем твою sessionmaker
        await promotions_service.daily_promo_check(db)

scheduler.add_job(daily_promo_task, 'cron', hour=0, minute=0)

@app.on_event("startup")
async def startup_event():
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()