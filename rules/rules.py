import discord
from discord.ext import commands
from cogs.utils.chat_formatting import box

class Rules:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rules", aliases=["RULES", "Rules"])
    async def rules(self):

        #Your code will go here
        msg = "RULE 1: Don't advertise any other mods. It's annoying to brag about other mod creators.\n\n"
        msg += "RULE 2: Do NOT mass mention Lord Consecro or any staff member. You will receive a mute.\n\n"
        msg += "RULE 3: Be respectful to staff member and supporters. Listen to them and follow their rules.\n\n"
        msg += "RULE 4: Use the channels for what they are for. That means actually following what the channel is for.\n\n"
        msg += "RULE 5: Advertising you're server or any other server is forbidden!"
        
        await self.bot.say(box(msg))


def setup(bot):
    bot.add_cog(Rules(bot))
