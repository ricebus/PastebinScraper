import time
from timeloop import Timeloop
from datetime import timedelta
from scraper import Scraper
import os
from pastesaver.db import DB
from pastesaver.file import File
from pymongo.errors import ConnectionFailure

mode = "db" if "SCRAPER_MODE" in os.environ and \
               os.environ["SCRAPER_MODE"].lower() == "db" else "file"
connection_string = os.environ["SCRAPER_CONN_STRING"] \
    if "SCRAPER_CONN_STRING" in os.environ \
    else "mongodb://127.0.0.1:27017/"
tl = Timeloop()


@tl.job(interval=timedelta(seconds=2))
def scrape_job_every_2m():
    print("scrape job current time: {}".format(time.ctime()))
    scraper = Scraper()
    pastes = scraper.run()
    saver = DB(connection_string) if mode == "db" else File()

    try:
        saver.save(pastes)
    except ConnectionFailure:
        print("MongoDB connection error")
    except PermissionError:
        print("File permission error")


if __name__ == "__main__":
    tl.start(block=True)
