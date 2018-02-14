import discord
from discord.ext import commands
from cogs.utils.chat_formatting import box

class Rules:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rules(self):
        """This does stuff!"""

		msg = "RULE 1: Don't advertise any other mods. It's annoying to brag about other mod creators.\n\n"
		
		await self.bot.say(msg)


def setup(bot):
    bot.add_cog(Rules(bot))
