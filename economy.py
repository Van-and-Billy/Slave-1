import casino
import discord
import economyInfo

economyInfo = economyInfo.economyInfo()


class economy:
    
    @staticmethod
    def condition(user, bet):
        return ((bet >= 50) and (user["stats"]["money"]) >= bet) or user["mod"]
    
    @staticmethod
    async def game(message, user, game):
        serverId = message.channel.guild.id
        userId = message.author.id
        mes = message.content.split(" ")
        try:
            bet = int(mes[1])
            value = int(mes[2])
            if economy.condition(user=user, bet=bet):
                result = game(bet, value)
                await message.channel.send(result)
                await economyInfo.editUserStats(serverId=serverId, userId=userId, money=result[0])
        except:
            pass

    @staticmethod
    async def balance(message, user):
        money = user["stats"]["money"]
        return await message.channel.send(f"Баланс <@{user['userId']}>: {money}$")
