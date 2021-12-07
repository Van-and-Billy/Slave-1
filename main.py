import os
import json


class main:
    
    def __init__(self):
        self.Settings = "/Settings.json"
        self.Servers = "/servers.json"
        
    def dataSave(self, Args: list = None, Point: int = None, Starttime: int = None, status: bool = None):
        data = [Args, Starttime, Point, status]
        names = ["args", "starttime", "duration", "status"]
        newdata = {
            "args": Args,
            "starttime": Starttime,
            "duration": Point,
            "status": status
        }
        with open(os.getcwd() + self.Settings, "r+", encoding="utf-8") as file:
            filedata = json.loads(file.readlines()[0])
        for x in range(len(data)):
            if data[x] is None:
                newdata[names[x]] = filedata[names[x]]
            else:
                newdata[names[x]] = data[x]
        with open(os.getcwd() + self.Settings, "w+", encoding="utf-8") as file:
            file.write(json.dumps(newdata))
        return True
    
    @staticmethod
    def end(minutes):
        os.system("shutdown /s /t " + str(minutes * 60))

    def getActiveStatus(self):
        with open(os.getcwd() + self.Settings, "r+", encoding="utf-8") as file:
            filedata = json.loads(file.readlines()[0])
        return filedata["status"]

    def getSettings(self):
        try:
            with open(os.getcwd() + self.Settings, "r+", encoding='utf-8') as file:
                data = json.loads((file.readlines())[0])
            return {
                "duration": data['duration'],
                "startTime": data['starttime']
            }
        except FileNotFoundError:
            with open(os.getcwd() + self.Settings, 'a+', encoding='utf-8') as file:
                file.write(json.dumps({"args": ['a', 'b'], "starttime": 3240, "duration": 300, "status": True}))
            return main.newGetInfo()

    def getServersInfo(self):
        try:
            with open(os.getcwd() + self.Servers, "r+", encoding='utf-8') as file:
                servers = json.loads((file.readlines())[0])
            serverIds = []
            for x in servers:
                serverIds.append(x["serverId"])
            return {
                "servers": servers,
                "serverIds": serverIds
            }
        except FileNotFoundError:
            with open(os.getcwd() + self.Servers, 'a+', encoding='utf-8') as file:
                file.write(json.dumps([{"serverId": 877119061866192916, "status": True,
                                        "modules": {"economy": True, "main": True, "global": True}}]))
            return main.newGetServersInfo()
        