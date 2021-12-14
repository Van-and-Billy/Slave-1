import discord
import os
import json
import main
import datetime
import time

main = main.main()
client = discord.Client()


class commands:
    
    def __init__(self):
        self.Servers = "/servers.json"
        
    @staticmethod
    async def help(message):
        await message.channel.send("В разработке.")
    
    async def checkServer(self, message, data):
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
            with open(os.getcwd() + self.Servers, 'w+', encoding='utf-8') as file:
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
    
    async def editModuleAccess(self, message, modules, data):
        module = message.content.split(" ")[1]
        if module in modules:
            serversData = data["servers"]
            serverIds = data["serverIds"]
            server = serversData[serverIds.index(message.channel.guild.id)]
            serverModuleInfo = server["modules"][module]
            value = (message.content.split(" ")[2].lower() == "true")
            if not (serverModuleInfo == value):
                serversData[serverIds.index(message.channel.guild.id)]["modules"][module] = value
                with open(os.getcwd() + self.Servers, 'w+', encoding='utf-8') as file:
                    file.write(json.dumps(serversData))
                await message.channel.send("Успешно.")
            else:
                return
