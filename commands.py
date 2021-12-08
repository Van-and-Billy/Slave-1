import discord
import os
import json
import main
import datetime
import time

main = main.main()
client = discord.Client()


class commands:
    
    @staticmethod
    async def info(message, getTime):
        # await client.wait_until_ready()
        if discord.utils.get(message.author.guild.roles, id=887655688724168754) in message.author.roles:
            infoTime = f'{str(datetime.timedelta(seconds=round(getTime())))}'
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
        # await client.wait_until_ready()
        await message.channel.send("В разработке.")
    
    @staticmethod
    async def activity(message, statusCode: bool):
        # await client.wait_until_ready()
        mess = ["Бот выключен.", "Бот включен."]
        if not main.getActiveStatus() == statusCode:
            if discord.utils.get(message.author.guild.roles, id=887655688724168754) in message.author.roles:
                main.dataSave(status=statusCode)
                await message.channel.send(mess[int(statusCode)])
    
    @staticmethod
    async def edit_point(message, edit):
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
            edit(end=starttime)
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
