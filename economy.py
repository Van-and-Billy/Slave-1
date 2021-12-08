import casino
import discord

casino = casino.Casino()


class economy:
    
    @staticmethod
    async def punch(message, user):
        mes = message.content.split(" ")
        try:
            if (int(mes[1]) >= 50) and (user["stats"]["money"]) >= int(mes[1]):
                result = casino.punch(bet=int(mes[1]), power=int(mes[2]))
                await message.channel.send(result)
                return result
        except:
            return [0, 0]
        