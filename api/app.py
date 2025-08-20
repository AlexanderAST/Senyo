from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.service.promotions_service import PromotionsService
from fastapi import FastAPI
from api.controller import hello_controller, client_controller, address_controller, point_logs_controller, referrals_controller, promotions_controller, make_appointment_controller, service_controller, place_type_controller

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
    async with AsyncSession(engine) as db:  # Или используй get_db, но для scheduler лучше sessionmaker
        await promotions_service.daily_promo_check(db)

scheduler.add_job(daily_promo_task, 'cron', hour=0, minute=0)
scheduler.start()