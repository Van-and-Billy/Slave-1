import timeEvents
import main
import commands
import economy
import economyInfo
import casino
import sys
import discord
# import asyncio
# import uuid
from config import token

client = discord.Client()
timeEvents = timeEvents.timeEvents()
main = main.main()
casino = casino.Casino()
economy = economy.economy()
economyInfo = economyInfo.economyInfo()
commands = commands.commands()


BOT_MODULES = ["main", "economy"]
BOT_MESSAGES = ["/info", "/pcOff", "/help", "/off", "/on", "/setPoint", "/moduleAccess", "/punch"]
BOT_COMMANDS = [
    {"func": commands.info, "args": [timeEvents.getTime], "module": "main"},
    {"func": commands.pc_off, "args": [], "module": "main"},
    {"func": commands.help, "args": [], "module": "global"},
    {"func": commands.activity, "args": [False], "module": "main"},
    {"func": commands.activity, "args": [True], "module": "main"},
    {"func": commands.edit_point, "args": [timeEvents.edit], "module": "main"},
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


@client.event
async def on_ready():
    print(f'bot started during {round(timeEvents.getTime(), 2)} sec')
    # channel = client.get_channel(877119061866192919)
    # await channel.send('<@455990052338794497>, компьютер включен.')


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
