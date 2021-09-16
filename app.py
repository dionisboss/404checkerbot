from utils.set_bot_commands import set_default_commands
from loader import scheduler
from data.config import admins
import requests
from loader import dp

async def parse_site(admins = admins):
    res = requests.request("GET", "http://92.38.160.97:8800")
    print(res.ok)
    if not res.ok:
        for admin in admins:
            dp.bot.send_message(admin, "Сайт упал")


def schedule_jobs():
    scheduler.add_job(parse_site, 'interval', seconds=2, args=(dp,))

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)
    schedule_jobs()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
