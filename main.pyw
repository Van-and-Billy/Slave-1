import sys
import os
import timeEvents
import threading
import json
# import asyncio
import discord
import datetime
import casino
import time
# import uuid
from config import token, ch

client = discord.Client()
timeEvents = timeEvents.timeEvents()


class Main:
    
    def __init__(self):
        self.nigger: int = 1
    
    @staticmethod
    def getActiveStatus():
        with open(os.getcwd() + "/Settings.json", "r+", encoding="utf-8") as file:
            filedata = json.loads(file.readlines()[0])
        return filedata["status"]
    
    @staticmethod
    def newGetServersInfo():
        global servers, serverIds
        try:
            with open(os.getcwd() + "/servers.json", "r+", encoding='utf-8') as file:
                servers = json.loads((file.readlines())[0])
            serverIds = []
            for x in servers:
                serverIds.append(x["serverId"])
            print(serverIds)
        except FileNotFoundError:
            with open(os.getcwd() + '/servers.json', 'a+', encoding='utf-8') as file:
                file.write(json.dumps([{"serverId": 877119061866192916, "status": True,
                                        "modules": {"economy": True, "main": True, "global": True}}]))
            return main.newGetServersInfo()
    
    @staticmethod
    def newGetInfo():
        global point, starttime, args
        try:
            with open(os.getcwd() + "/Settings.json", "r+", encoding='utf-8') as file:
                data = json.loads((file.readlines())[0])
            args = data['args']
            point = data['duration']
            starttime = data['starttime']
        except (FileNotFoundError, IndexError):
            with open(os.getcwd() + '/Settings.json', 'a+', encoding='utf-8') as file:
                file.write(json.dumps({"args": ['a', 'b'], "starttime": 3240, "duration": 300, "status": True}))
            return main.newGetInfo()
    
    @staticmethod
    def newsave(Args: list = None, Point: int = None, Starttime: int = None, status: bool = None):
        data = [Args, Starttime, Point, status]
        names = ["args", "starttime", "duration", "status"]
        newdata = {
            "args": Args,
            "starttime": Starttime,
            "duration": Point,
            "status": status
        }
        with open(os.getcwd() + "/Settings.json", "r+", encoding="utf-8") as file:
            filedata = json.loads(file.readlines()[0])
        for x in range(len(data)):
            if data[x] is None:
                newdata[names[x]] = filedata[names[x]]
            else:
                newdata[names[x]] = data[x]
        with open(os.getcwd() + "/Settings.json", "w+", encoding="utf-8") as file:
            file.write(json.dumps(newdata))
        return True
    
    @staticmethod
    def end(minutes):
        esc = minutes * 60
        os.system("shutdown /s /t " + str(esc))


class commands:
    
    def __init__(self):
        self.niggers: int = 0
    
    @staticmethod
    async def info(message):
        global Time
        await client.wait_until_ready()
        if discord.utils.get(message.author.guild.roles, id=887655688724168754) in message.author.roles:
            infoTime = f'{str(datetime.timedelta(seconds=round(timeEvents.getTime())))}'
            with open(os.getcwd() + "/Settings.json", "r+", encoding="utf-8") as file:
                filedata = json.loads(file.readlines()[0])
            status = filedata["status"]
            await message.channel.send("```python\n{" + f'\n"time": {infoTime},\n"status": {status}' + "\n}\n```")
    
    @staticmethod
    async def pc_off(message):
        if message.author.id == 455990052338794497:
            main.end(minutes=1)
            await message.channel.send('Компьютер будет выключен через 1 минуту!')
    
    @staticmethod
    async def help(message):
        await client.wait_until_ready()
        await message.channel.send("В разработке.")
    
    @staticmethod
    async def activity(message, statusCode: bool):
        await client.wait_until_ready()
        mess = ["Бот выключен.", "Бот включен."]
        if not main.getActiveStatus() == statusCode:
            if discord.utils.get(message.author.guild.roles, id=887655688724168754) in message.author.roles:
                main.newsave(status=statusCode)
                await message.channel.send(mess[int(statusCode)])
    
    @staticmethod
    async def edit_point(message):
        global point, starttime
        if discord.utils.get(message.author.guild.roles, id=887655688724168754) in message.author.roles:
            mess = message.content.split(' ')
            point2 = mess[1].lower()
            if point2 == 'stock':
                point = 300
                starttime = 3240
            else:
                try:
                    point = int(mess[2])
                    starttime = int(mess[1])
                except:
                    return
            timeEvents.edit(end=starttime)
            main.newsave(Point=point, Starttime=starttime)
            await message.channel.send('Успешно.')
        else:
            await message.channel.send('Доступ запрещен.')
    
    @staticmethod
    def pointembed(sec: float):
        tms = time.strftime("%M:%S", time.gmtime(sec))
        embed = discord.Embed(type="rich", colour=discord.Color.blurple(), description=f'Point of No Return {tms}')
        return embed
    
    @staticmethod
    @timeEvents.event
    async def on_end():
        global point, starttime
        channel = client.get_channel(880411406929891349)
        if main.getActiveStatus():
            message = await channel.send(embed=commands.pointembed(sec=point))
            ftime = int(timeEvents.getTime() + point)
            while True:
                realTime = timeEvents.getTime()
                if ftime - realTime <= 0:
                    main.end(minutes=1)
                    await message.delete()
                    sys.exit()
                else:
                    await message.edit(content=f"<@455990052338794497>",
                                       embed=commands.pointembed(sec=(ftime - realTime)))
                time.sleep(0.85)
    
    @staticmethod
    async def checkServer(message):
        global servers, serverIds
        if (message.channel.guild.id in serverIds) is False:
            servers.append({"serverId": message.channel.guild.id, "status": True,
                            "modules": {"economy": True, "main": False, "global": True}})
            serverIds.append(message.channel.guild.id)
            with open(os.getcwd() + '/servers.json', 'w+', encoding='utf-8') as file:
                file.write(json.dumps(servers))
    
    @staticmethod
    async def commandAccess(message, module):
        index = serverIds.index(message.channel.guild.id)
        server = servers[index]
        return server["modules"][module]
    
    @staticmethod
    async def editModuleAccess(message, modules):
        global servers
        module = message.content.split(" ")[1]
        if module in modules:
            server = servers[serverIds.index(message.channel.guild.id)]
            serverModuleInfo = server["modules"][module]
            value = (message.content.split(" ")[2].lower() == "true")
            if not (serverModuleInfo == value):
                servers[serverIds.index(message.channel.guild.id)]["modules"][module] = value
                with open(os.getcwd() + '/servers.json', 'w+', encoding='utf-8') as file:
                    file.write(json.dumps(servers))
                await message.channel.send("Успешно.")
            else:
                return


class economyInfo:
    
    def __init__(self):
        self.nigger: int = 0
    
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


class economy:
    
    def __init__(self):
        self.nigger: int = 0
    
    @staticmethod
    async def punch(message, user):
        mes = message.content.split(" ")
        if (int(mes[1]) >= 50) and (user["stats"]["money"]) >= int(mes[1]):
            try:
                result = casino.punch(bet=int(mes[1]), power=int(mes[2]))
            except:
                return [0, 0]
            await message.channel.send(result)
            return result


main = Main()
commands = commands()
economyInfo = economyInfo()
economy = economy()
casino = casino.Casino()


@timeEvents.event
async def on_start():
    main.newGetInfo()
    main.newGetServersInfo()
    print('eee')


@client.event
async def on_ready():
    main.newsave(status=False)
    channel = client.get_channel(877119061866192919)
    # member = 'Sally Star#1482'
    userId: int = 455990052338794497
    await channel.send(f'<@{userId}>, компьютер включен.')
    # client.loop.create_task()
    print(f'bot started during {round(timeEvents.getTime(), 2)} sec')


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    modules = ["main", "economy"]
    mes = ["/info", "/pcOff", "/help", "/off", "/on", "/setPoint", "/moduleAccess", "/punch"]
    com = [
        {"func": commands.info, "args": [message], "module": "main"},
        {"func": commands.pc_off, "args": [message], "module": "main"},
        {"func": commands.help, "args": [message], "module": "global"},
        {"func": commands.activity, "args": [message, False], "module": "main"},
        {"func": commands.activity, "args": [message, True], "module": "main"},
        {"func": commands.edit_point, "args": [message], "module": "main"},
        {"func": commands.editModuleAccess, "args": [message, modules], "module": "global"},
        {"func": economy.punch, "args": [message], "module": "economy"}
        ]
    
    if message.content.startswith("/"):
        await commands.checkServer(message)
        serverId = message.channel.guild.id
        userId = message.author.id
        if (message.content.split(" ")[0]) in mes:
            a = mes.index((message.content.split(" ")[0]))
            if await commands.commandAccess(message, com[a]["module"]) is True:
                if com[a]["module"] == "economy" and (await economyInfo.checkUser(serverId=serverId, userId=userId)):
                    user = await economyInfo.getUserStats(serverId=serverId, userId=userId)
                    result = await com[a]["func"](*(com[a]["args"]), user=user)
                    await economyInfo.editUserStats(serverId=serverId, userId=userId, money=result[0])
                else:
                    await com[a]["func"](*(com[a]["args"]))
        

timeEvents.run()
client.run(token)
