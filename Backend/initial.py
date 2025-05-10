# Run in Python shell
from scraper import CarScraper
from trainer import CarModelTrainer

# First-time data scrape
scraper = CarScraper()
scraper.run()

# Initial model training
trainer = CarModelTrainer()
trainer.run_training()