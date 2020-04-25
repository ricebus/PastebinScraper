import time
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()


@tl.job(interval=timedelta(minutes=2))
def scrape_job_every_2m():
    print("scrape job current time: {}".format(time.ctime()))


if __name__ == "__main__":
    tl.start(block=True)
