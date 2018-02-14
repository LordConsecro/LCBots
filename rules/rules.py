import discord
from discord.ext import commands
from cogs.utils.chat_formatting import box

class Rules:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def rules(self, ctx):
        """This does stuff!"""

        #Your code will go here
		msg = "RULE 1: Don't advertise any other mods. It's annoying to brag about other mod creators.\n\n"
		
		await self.bot.say(box(msg))


def setup(bot):
    bot.add_cog(Rules(bot))
