import os
import json


class main:
    
    def __init__(self):
        self.Servers = (os.getcwd() + "/servers.json")
        
    def getServersInfo(self):
        try:
            with open(self.Servers, "r+", encoding='utf-8') as file:
                servers = json.loads((file.readlines())[0])
            serverIds = []
            for x in servers:
                serverIds.append(x["serverId"])
            return {
                "servers": servers,
                "serverIds": serverIds
            }
        except FileNotFoundError:
            with open(self.Servers, 'a+', encoding='utf-8') as file:
                file.write(json.dumps([{"serverId": 877119061866192916, "status": True,
                                        "modules": {"economy": True, "main": True, "global": True}}]))
            return main.getServersInfo(self)
        