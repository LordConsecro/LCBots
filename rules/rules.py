import discord
from discord.ext import commands

class Rules:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def rules(self, ctx):
        """This does stuff!"""

		msg = "RULE 1: Don't advertise any other mods. It's annoying to brag about other mod creators."
		
		await self.bot.say(msg)


def setup(bot):
    bot.add_cog(Rules(bot))
