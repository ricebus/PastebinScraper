import time
from timeloop import Timeloop
from datetime import timedelta
from scraper import Scraper
from paste import PasteEncoder
import json
import os

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
    if mode == "file":
        save_to_file(pastes)
    else:
        save_to_db(pastes, connection_string)


def save_to_db(pastes, connection_string):
    from pymongo.errors import ConnectionFailure
    try:
        col = prepare_db(connection_string)
        new_pastes = remove_existing_pastes(col,pastes)
        dict = PasteEncoder.default(None, new_pastes)
        if len(dict) != 0:
            print(dict)
            col.insert_many(dict)
        return True
    except ConnectionFailure:
        print("MongoDB connection error")
        return False


def prepare_db(connection_string):
    import pymongo
    mongo = pymongo.MongoClient(connection_string)
    db = mongo["pastedb"]
    col = db["pastes"]
    col.create_index("id", unique=True)
    return col

def remove_existing_pastes(col, pastes):
    clean = [paste for paste in pastes if col.find_one({"id": paste.id}) is None]
    return clean

def save_to_file(pastes, path=""):
    try:
        filename = "pastes" + time.strftime("%Y-%m-%d.%H-%M-%S") + ".json"
        location = os.path.join(path, filename)
        f = open(location, "a")
        json_array = json.dumps(pastes, cls=PasteEncoder)
        f.write(json_array)
        f.close()
        return True
    except PermissionError:
        print("File permission error (" + location + ")")
        return False


if __name__ == "__main__":
    tl.start(block=True)
