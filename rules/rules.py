import discord
from discord.ext import commands

class Rules:

    def __init__(self, bot):
        self.bot = bot
		
		self.msg = "RULE 1: Don't advertise any other mods. It's annoying to brag about other mod creators."

    @commands.command(name="rules", aliases=["RULES", "Rules"])
    async def rules(self):
        """This does stuff!"""
		
		await self.bot.say(self.msg)


def setup(bot):
    bot.add_cog(Rules(bot))
