import os
import json
import main
import commands
import economy
import economyInfo
import sys
import discord
# import asyncio
# import uuid

client = discord.Client()
main = main.main()
economy = economy.economy()
economyInfo = economyInfo.economyInfo()
commands = commands.commands()

BOT_MODULES = ["economy"]
BOT_MESSAGES = ["/help", "/moduleAccess", "/punch"]
BOT_COMMANDS = [
    {"func": commands.help, "args": [], "module": "global"},
    {"func": commands.editModuleAccess, "args": [BOT_MODULES], "module": "global"},
    {"func": economy.punch, "args": [], "module": "economy"}
]


@client.event
async def on_ready():
    # print(f' bot started during {round(timeEvents.getTime(), 2)} sec')
    print(main.getServersInfo())


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
        await client.wait_until_ready()
        await checkMessage(message=message, messages=BOT_MESSAGES, command=BOT_COMMANDS)


def getToken():
    with open(os.getcwd() + "/config.json", "r+", encoding='utf-8') as file:
        config = json.loads((file.readlines())[0])
    return config["token"]


client.run(getToken())
