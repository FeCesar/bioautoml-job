import json


class UpdateStatusVO:
    def __init__(self, status, process_id):
        self.processId = process_id
        self.status = status

    def to_json(self):
        return json.dumps(self.__dict__)