import asyncio
import threading
import time
import os
import json
from syncer import sync


def getEnd():
    with open(os.getcwd() + "/Settings.json", "r+", encoding='utf-8') as file:
        data = json.loads((file.readlines())[0])
    return data['starttime']


class timeEvents:
    
    def __init__(self):
        self.end = getEnd()
        self.Time: int = None
    
    def event(self, function):
        if function.__name__ not in ["on_end", "on_start"]:
            raise TypeError("Incorrect function name.")
        setattr(self, function.__name__, function)
        return function
    
    @sync
    async def callbacks(self, function):
        await function()
    
    def timer(self):
        startTime = time.time()
        while True:
            self.Time = time.time() - startTime
            if self.Time >= self.end:
                timeEvents.callbacks(self, self.on_end)
            time.sleep(0.334)
    
    def run(self):
        threading.Thread(target=timeEvents.timer, args=(self, )).start()
        if getattr(self, "on_start", False):
            timeEvents.callbacks(self, self.on_start)
    
    def edit(self, end):
        self.end = end
        
    def getTime(self):
        return self.Time
    