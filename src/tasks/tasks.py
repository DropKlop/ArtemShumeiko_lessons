import asyncio
import os.path
from time import sleep
from PIL import Image

from src.database import async_sessionmaker_maker_null_pull
from src.tasks.celery_app import celery_app
from src.utils.db_manager import DBManager


@celery_app.task
def test_task():
    sleep(5)
    print("harosh")

#@celery_app.task
def resize_image(path: str):
    sizes = [1000, 500, 200]
    output_folder = "src/static/images"

    img= Image.open(path)

    base_name = os.path.basename(path)
    name, ext = os.path.splitext(base_name)
    print("я начал")
    for size in sizes:
        img_resized = img.resize((size, int(img.height * ( size / img.width))), Image.Resampling.LANCZOS)

        new_file_name = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_folder, new_file_name)

        img_resized.save(output_path)
    print("я все")


async def get_bookings_with_today_checkin_helper():
    async with DBManager(session_factory=async_sessionmaker_maker_null_pull) as db:
        bookings = await db.bookings.get_booking_with_today_check_in()
        print(bookings)


@celery_app.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())