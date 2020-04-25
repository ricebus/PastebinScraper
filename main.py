import time
from timeloop import Timeloop
from datetime import timedelta
from scraper import Scraper
import json

tl = Timeloop()


@tl.job(interval=timedelta(seconds=5))
def scrape_job_every_2m():
    print("scrape job current time: {}".format(time.ctime()))
    scraper = Scraper()
    pastes = scraper.parse_main_page()
    f = open("pastes" + time.strftime("%Y-%m-%d.%H-%M-%S") + ".json", "a")
    for paste in pastes:
        json_str = json.dumps(paste.__dict__)
        f.write(json_str)
    f.close()


if __name__ == "__main__":
    tl.start(block=True)
