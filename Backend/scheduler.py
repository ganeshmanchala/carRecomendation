
# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from scraper import CarScraper
from trainer import CarModelTrainer
import atexit
import os
from app import app  # Import the Flask app for debug flag
from database import CarDatabase

def scheduled_job():
    print("\n=== Starting daily update ===")
    try:
        # Run scraper: fetch new car data and upsert into the DB
        scraper = CarScraper()
        scraper.run()
       
        # Train new models using the updated car data
        trainer = CarModelTrainer()
        trainer.run_training()
       
        # Delete old car data and prune model versions (keep only latest)
        db = CarDatabase()
        db.prune_old_cars()
        db.prune_old_models()
        db.close()
       
        print("=== Daily update completed successfully ===")
    except Exception as e:
        print(f"!!! Scheduled job failed: {str(e)} !!!")

def initialize_scheduler():
    # Only start scheduler in the main process
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.debug:
        scheduler = BackgroundScheduler(daemon=True)
        scheduler.add_job(
            scheduled_job,
            CronTrigger(hour=3, timezone='UTC'),
            misfire_grace_time=3600
        )
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())

# Initialize scheduler when this module is imported
initialize_scheduler()
