from apscheduler.schedulers.background import BackgroundScheduler

from app.services.reminder_service import run_reminder_scan

scheduler = BackgroundScheduler(timezone="Asia/Shanghai")


def start_scheduler(app):
    if scheduler.running:
        return

    hour = app.config.get("REMINDER_SCAN_HOUR", 1)

    def task_wrapper():
        with app.app_context():
            run_reminder_scan()

    scheduler.add_job(task_wrapper, "cron", hour=hour, minute=0, id="daily_reminder_scan", replace_existing=True)
    scheduler.start()
