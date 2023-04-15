import json
from datetime import datetime


class ErrorHandler:

    def __init__(self, error_type, message, process_id):
        self.errorType = error_type
        self.message = message
        self.processId = process_id
        self.referenceDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_json(self):
        return json.dumps(self.__dict__)
