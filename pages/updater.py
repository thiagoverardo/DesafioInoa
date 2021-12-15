from apscheduler.schedulers.background import BackgroundScheduler
from .update_stock_price import update_something


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_something, 'interval', hours=12)
    scheduler.start()