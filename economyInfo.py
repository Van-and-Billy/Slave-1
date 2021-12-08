import os
import json


class economyInfo:
    
    def __init__(self):
        self.path = "Servers"
    
    @staticmethod
    def userForm(userId: int):
        form = {"userId": userId, "stats": {"exp": 0, "money": 0, "bank": 0}}
        return form
    
    @staticmethod
    async def checkServer(serverId: int):
        try:
            with open(os.getcwd() + f"/Servers/{serverId}.json", "r+", encoding="utf-8") as server:
                users = json.loads((server.readlines())[0])
            return users
        except FileNotFoundError:
            with open(os.getcwd() + f"/Servers/{serverId}.json", "a+", encoding="utf-8") as server:
                server.write(json.dumps([{"userId": 877116735092838421, "stats": {"exp": 0, "money": 0, "bank": 0}}]))
            return await economyInfo.checkServer(serverId)
    
    @staticmethod
    def serverUsers(users: list) -> list:
        serverUsersIds = []
        for x in users:
            serverUsersIds.append(x["userId"])
        return serverUsersIds
    
    @staticmethod
    async def checkUser(serverId: int, userId: int):
        users = await economyInfo.checkServer(serverId)
        ids = economyInfo.serverUsers(users)
        if not (userId in ids):
            with open(os.getcwd() + f"/Servers/{serverId}.json", "w+", encoding="utf-8") as server:
                form = economyInfo.userForm(userId)
                users.append(form)
                server.write(json.dumps(users))
            return await economyInfo.checkUser(serverId, userId)
        else:
            return True
    
    @staticmethod
    async def getUserStats(userId: int, serverId: int):
        users = await economyInfo.checkServer(serverId)
        ids = economyInfo.serverUsers(users)
        return users[(ids.index(userId))]
    
    @staticmethod
    async def editUserStats(userId: int, serverId: int, exp: int = None, money: int = None, bank: int = None):
        users = await economyInfo.checkServer(serverId)
        ids = economyInfo.serverUsers(users)
        data = [exp, money, bank]
        names = ["exp", "money", "bank"]
        newstats = {
            "exp": exp,
            "money": money,
            "bank": bank
        }
        user = users[ids.index(userId)]
        for x in range(len(data)):
            if data[x] is None:
                newstats[names[x]] = user["stats"][names[x]]
            else:
                newstats[names[x]] = user["stats"][names[x]] + data[x]
        newdata = {
            "userId": userId,
            "stats": newstats
        }
        users[ids.index(userId)] = newdata
        with open(os.getcwd() + f"/Servers/{serverId}.json", "w+", encoding="utf-8") as server:
            server.write(json.dumps(users))
            