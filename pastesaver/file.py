from .isaver import ISaver
from paste import PasteEncoder
import time
import os
import json


class File(ISaver):
    def __init__(self, path=""):
        self.path = path

    def save(self, pastes):
        filename = "pastes" + time.strftime("%Y-%m-%d.%H-%M-%S") + ".json"
        location = os.path.join(self.path, filename)
        f = open(location, "a")
        json_array = json.dumps(pastes, cls=PasteEncoder)
        f.write(json_array)
        f.close()
