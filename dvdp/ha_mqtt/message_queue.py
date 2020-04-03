import asyncio
from copy import copy
from datetime import timedelta, datetime


class MessageQueue:
    def __init__(self, max_age=timedelta(seconds=10)):
        self.__max_age = max_age
        self.__queue = list()

    def __len__(self):
        return len(self.__queue)

    def add(self, topic, value):
        self.__queue.append([topic, value, datetime.now()])

    async def get(self, topic):
        values = []
        while not values:
            now = datetime.now()
            self.__queue = [
                [topic2, value, timestamp]
                for topic2, value, timestamp in self.__queue
                if now - timestamp < self.__max_age
            ]
            for topic2, value, timestamp in self.__queue:
                if topic2 == topic:
                    values = [topic2, value, timestamp]
                    value2 = copy(value)
                    self.__queue.remove(values)
                    return value2
            await asyncio.sleep(0)