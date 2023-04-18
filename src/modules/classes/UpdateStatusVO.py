import json
from datetime import datetime


class UpdateStatusVO:
    def __init__(self, status, process_id):
        self.processId = process_id
        self.status = status
        self.referenceDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_json(self):
        return json.dumps(self.__dict__)
