import discord
from discord.ext import commands
from cogs.utils.chat_formatting import box

class Rules:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rules(self):
        """This does stuff!"""

        #Your code will go here
		msg = "RULE 1: Don't advertise any other mods. It's annoying to brag about other mod creators.\nRULE 2: Do NOT mass mention Lord Consecro or any staff member. You will receive a mute.\nRULE 3: Be respectful to staff member and supporters. Listen to them and follow their rules.\nRULE 4: Use the channels for what they are for. That means actually following what the channel is for.\nRULE 5: Advertising you're server or any other server is forbidden!"
		
		await self.bot.say(box(msg))


def setup(bot):
    bot.add_cog(Rules(bot))
