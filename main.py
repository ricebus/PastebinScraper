import time
from timeloop import Timeloop
from datetime import timedelta
from scraper import Scraper
from paste import PasteEncoder
import json

tl = Timeloop()


@tl.job(interval=timedelta(seconds=5))
def scrape_job_every_2m():
    print("scrape job current time: {}".format(time.ctime()))
    scraper = Scraper()
    pastes = scraper.run()
    f = open("pastes" + time.strftime("%Y-%m-%d.%H-%M-%S") + ".json", "a")
    for paste in pastes:
        if paste is not None:
            jsontxt = json.dumps(paste, cls=PasteEncoder)
            f.write(jsontxt)
    f.close()


if __name__ == "__main__":
    tl.start(block=True)
