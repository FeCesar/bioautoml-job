import json
from datetime import datetime


class ProcessResult:

    def __init__(self, process_id):
        self.processId = process_id
        self.referenceDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_json(self):
        return json.dumps(self.__dict__)
