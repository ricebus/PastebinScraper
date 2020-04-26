from .isaver import ISaver
from paste import PasteEncoder
import pymongo


class DB(ISaver):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.col = self.prepare_db()

    def save(self, pastes):
        new_pastes = self.remove_existing_pastes(pastes)
        dict = PasteEncoder.default(None, new_pastes)
        if len(dict) != 0:
            self.col.insert_many(dict)

    def prepare_db(self):
        mongo = pymongo.MongoClient(self.connection_string)
        db = mongo["pastedb"]
        col = db["pastes"]
        col.create_index("id", unique=True)
        return col

    def remove_existing_pastes(self, pastes):
        clean = [paste for paste in pastes
                 if self.col.find_one({"id": paste.id}) is None]
        return clean
