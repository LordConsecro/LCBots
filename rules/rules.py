from discord.ext import commands

rules = {
    "Don't advertise any other mods from Nexus or Bethesda.net here. It's annoying to brag about other mod creators.",
	"Do NOT mass mention Lord Consecro or any staff member. You will receive a mute.",
	"Be respectful to staff member and supporters. Listen to them and follow their rules.",
	"Use the channels for what they are for. That means actually following what the channel is for.",
	"Advertising you're server or any other server is forbidden! If you are caught, you will receive a mute."
}


class Rules:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rules(self):
        """Rules"""
        for number, rule in enumerate(rules, 1):
			await self.bot.say("RULE {}: {}".format(number, rule))


def setup(bot):
    n = Rules(bot)
    bot.add_cog(n)
