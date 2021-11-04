import datetime
import enum
import json


class Frequencies(enum.Enum):
    second = 0
    minute = 1
    hour = 2
    day = 3
    week = 4
    month = 5


class JobConfiguration:
    def __init__(self):
        self.frequency = Frequencies.day
        self.everyFrequency = 1
        self.volume = 1.0
        self.startDate = datetime.datetime.now()
        self.startTime = '00:00'

    def __dict__(self):
        return {
            'frequency': self.frequency.value,
            'everyFrequency': self.everyFrequency,
            'volume': self.volume,
            'startDate': self.startDate.isoformat(),
            'startTime': self.startTime,
        }

    def write(self, file_path):
        with open(file_path, 'w') as file:
            file.write(json.dumps(self.__dict__()))

    @staticmethod
    def read(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
        json_string = json.loads(data)
        return JobConfiguration.from_json(json_string)

    @staticmethod
    def from_json(json_object):
        config = JobConfiguration()
        config.frequency = Frequencies(json_object['frequency'])
        config.everyFrequency = json_object['everyFrequency']
        config.volume = json_object['volume']
        config.startDate = datetime.datetime.fromisoformat(json_object['startDate'])
        config.startTime = json_object['startTime']

        return config
