import timeEvents
import main
import sys
import os
import threading
import json
# import asyncio
import discord
import datetime
import casino
import time
# import uuid
import config
from config import token, ch

client = discord.Client()
timeEvents = timeEvents.timeEvents()
main = main.main()
casino = casino.Casino()


class commands:
    
    def __init__(self):
        self.niggers: int = 0
    
    @staticmethod
    async def info(message):
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
                main.dataSave(status=statusCode)
                await message.channel.send(mess[int(statusCode)])
    
    @staticmethod
    async def edit_point(message):
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
            main.dataSave(Point=point, Starttime=starttime)
            await message.channel.send('Успешно.')
        else:
            await message.channel.send('Доступ запрещен.')
    
    @staticmethod
    def pointembed(sec: float):
        tms = time.strftime("%M:%S", time.gmtime(sec))
        embed = discord.Embed(type="rich", colour=discord.Color.blurple(), description=f'Point of No Return {tms}')
        return embed
    
    @staticmethod
    async def checkServer(message, data):
        serversData = data["servers"]
        serverIds = data["serverIds"]
        if (message.channel.guild.id in serverIds) is False:
            serversData.append({
                "serverId": message.channel.guild.id,
                "status": True,
                "modules": {
                    "economy": True,
                    "main": False,
                    "global": True
                }
            })
            serverIds.append(message.channel.guild.id)
            with open(os.getcwd() + '/servers.json', 'w+', encoding='utf-8') as file:
                file.write(json.dumps(serversData))
        return {
            "servers": serversData,
            "serverIds": serverIds
        }
    
    @staticmethod
    async def commandAccess(message, module, data):
        serverIds = data["serverIds"]
        serversData = data["servers"]
        index = serverIds.index(message.channel.guild.id)
        server = serversData[index]
        return server["modules"][module]
    
    @staticmethod
    async def editModuleAccess(message, modules, data):
        module = message.content.split(" ")[1]
        if module in modules:
            serversData = data["servers"]
            serverIds = data["serverIds"]
            server = serversData[serverIds.index(message.channel.guild.id)]
            serverModuleInfo = server["modules"][module]
            value = (message.content.split(" ")[2].lower() == "true")
            if not (serverModuleInfo == value):
                serversData[serverIds.index(message.channel.guild.id)]["modules"][module] = value
                with open(os.getcwd() + '/servers.json', 'w+', encoding='utf-8') as file:
                    file.write(json.dumps(serversData))
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


commands = commands()
economyInfo = economyInfo()
economy = economy()


BOT_MODULES = ["main", "economy"]
BOT_MESSAGES = ["/info", "/pcOff", "/help", "/off", "/on", "/setPoint", "/moduleAccess", "/punch"]
BOT_COMMANDS = [
    {"func": commands.info, "args": [], "module": "main"},
    {"func": commands.pc_off, "args": [], "module": "main"},
    {"func": commands.help, "args": [], "module": "global"},
    {"func": commands.activity, "args": [False], "module": "main"},
    {"func": commands.activity, "args": [True], "module": "main"},
    {"func": commands.edit_point, "args": [], "module": "main"},
    {"func": commands.editModuleAccess, "args": [BOT_MODULES], "module": "global"},
    {"func": economy.punch, "args": [], "module": "economy"}
]


@timeEvents.event
async def on_start():
    main.getSettings()
    main.getServersInfo()
    main.dataSave(status=False)


@timeEvents.event
async def on_end():
    settings = main.getSettings()
    channel = client.get_channel(880411406929891349)
    if main.getActiveStatus():
        message = await channel.send(embed=commands.pointembed(sec=settings["duration"]))
        ftime = int(timeEvents.getTime() + settings["duration"])
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


# @client.event
# async def on_ready():
    # channel = client.get_channel(877119061866192919)
    # await channel.send('<@455990052338794497>, компьютер включен.')
    # print(f 'bot started during {round(timeEvents.getTime(), 2)} sec')


async def checkMessage(message, messages, command):
    data = await commands.checkServer(message, main.getServersInfo())
    serverId = message.channel.guild.id
    userId = message.author.id
    if (message.content.split(" ")[0]) in messages:
        i = messages.index((message.content.split(" ")[0]))
        command = command[i]
        if await commands.commandAccess(message, command["module"], data):
            if command["module"] == "economy" and (await economyInfo.checkUser(serverId=serverId, userId=userId)):
                user = await economyInfo.getUserStats(serverId=serverId, userId=userId)
                result = await command["func"](*(command["args"]), user=user, message=message)
                await economyInfo.editUserStats(serverId=serverId, userId=userId, money=result[0])
            else:
                if message.content.startswith("/moduleAccess"):
                    await command["func"](message, *(command["args"]), data=data)
                else:
                    await command["func"](message, *(command["args"]))
    
    
@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content.startswith("/"):
        await checkMessage(message=message, messages=BOT_MESSAGES, command=BOT_COMMANDS)
    
    
timeEvents.run()
client.run(token)
