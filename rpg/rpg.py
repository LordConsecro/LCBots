#This is all your imports, if you have to import code from other scripts
import discord
from discord.ext import commands
from discord.utils import find
from __main__ import send_cmd_help
import platform, asyncio, string, operator, random, textwrap
import os, re, aiohttp
from .utils.dataIO import fileIO
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
import time
import json
import random
import re
try:
    import scipy
    import scipy.misc
    import scipy.cluster
except:
    pass

#this fetches our prefix for the server
prefix = fileIO("data/red/settings.json", "load")['PREFIXES']

#this is just a dev ID 
dev = ["312127693242236928"]

#this calls the main bot cog (the name per say)
class RPG:
    def __init__(self, bot):
        self.bot = bot

    def _is_mention(self,user):
        if "mention" not in self.settings.keys() or self.settings["mention"]:
            return user.mention
        else:
            return user.name

    async def check_answer(self, ctx, valid_options):

        answer = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)

        if answer.content.lower() in valid_options:
            return answer.content
            

        elif answer.content in valid_options:
            return answer.content

        elif answer.content.upper() in valid_options:
            return answer.content

        else:
            return await self.check_answer(ctx, valid_options)
        

    #this is your actual command, and where you would put aliases and stuff, the @command.group lets the script know this is the MAIN command
    @commands.group(pass_context = True, aliases=["RPG", "R"])
    async def rpg(self, ctx):
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            return
            
    # this is the main menu
    @rpg.command(pass_context = True)
    async def menu(self, ctx):
        channel = ctx.message.channel
        server = channel.server
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        
        menu_list = []
        if userinfo["race"] == "None":
            menu_list.append("1: New Character")
        elif not userinfo["race"] == "None":
            menu_list.append("1: Reset Character")
        
        em = discord.Embed(title="|====[ {} ]====|".format(user.name), description="```diff\n\n- Select an Option:\n+ {}```".format("\n+ ".join(menu_list)), color=0xffffff)
        await self.bot.say(embed=em)
        
        answer0 = await self.check_answer(ctx, ["1", "2", "!rpg"])

        if answer0 == "!rpg":
            return
            
        elif answer0 == "1":
        
            await self._create_user(user, server)

            if not userinfo["class"] == "None" and not userinfo["race"] == "None":
                await self.bot.reply("Are you sure you want to restart?")
                answer1 = await self.check_answer(ctx, ["y", "yes", "n", "no", "!rpg"])

                if answer1 == "!rpg":
                    pass
                elif answer1 == "y" or answer1 == "Y" or answer1 == "yes" or answer1 == "Yes":
                    userinfo["gold"] = 0
                    userinfo["race"] = "None"
                    userinfo["class"] = "None"
                    userinfo["enemieskilled"] = 0
                    userinfo["equip"] = "None"
                    userinfo["inventory"] = []
                    userinfo["health"] = 100
                    userinfo["deaths"] = 0
                    userinfo["hp_potions"] = 0
                    userinfo["inguild"] = "None"
                    userinfo["guildhash"] = 0
                    userinfo["lootbag"] = 0
                    userinfo["name"] = user.name
                    userinfo["location"] = "Golden Temple"
                    userinfo["selected_enemy"] = "None"
                    userinfo["daily_block"] = 0
                    userinfo["rest_block"] = 0
                    userinfo["in_dungeon"] = "False"
                    userinfo["duneon_enemy_hp"] = 0
                    userinfo["dungeon_enemy"] = "None"
                    userinfo["wearing"] = "None"
                    userinfo["keys"] = 0
                    userinfo["roaming"] = "False"
                    userinfo["lvl"] = 0
                    userinfo["chop_block"] = 0
                    userinfo["mine_block"] = 0
                    userinfo["in_party"] = []
                    userinfo["thirst"] = 0
                    userinfo["hunger"] = 0
                    userinfo["tiredness"] = 0
                    fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                    await self.bot.say("{}, you have been reset! Please use `!rpg` again.".format(userinfo["name"]))
                    return
                elif answer0 == "n" or answer0 == "N" or answer0 == "no" or answer0 == "No":
                    await self.bot.say("Restart Canceled")
                    return
            
            race_list = []
            race_list.append("1: Human")
            race_list.append("2: Orc")
            race_list.append("3: Elf")
            
            em = discord.Embed(title="|====[ {} ]====|".format(user.name), description="```diff\n\n- What is your race:\n+ {}```".format("\n+ ".join(race_list)), color=0xffffff)
            await self.bot.say(embed=em)

            answer1 = await self.check_answer(ctx, ["1", "human", "2", "orc", "3", "elf", "!rpg"])

            if answer1 == "!rpg":
                pass
            elif answer1 == "1" or answer1 == "human":
                userinfo["race"] = "Human"
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
            elif answer1 == "2" or answer1 == "orc":
                userinfo["race"] = "Orc"
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
            elif answer1 == "3" or answer1 == "elf":
                userinfo["race"] = "Elf"
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)

            class_list = []
            class_list.append("1: Ranger")
            class_list.append("2: Paladin")
            class_list.append("3: Mage")
            class_list.append("4: Thief")
            
            em = discord.Embed(title="|====[ {} ]====|".format(user.name), description="```diff\n\n- What is your class:\n+ {}```".format("\n+ ".join(class_list)), color=0xffffff)
            await self.bot.say(embed=em)

            answer2 = await self.check_answer(ctx, ["1", "ranger", "2", "paladin", "3", "mage", "4", "thief", "!rpg"])

            if answer2 == "!rpg":
                return

            elif answer2 == "1" or answer2 == "ranger":
                userinfo["class"] = "Ranger"
                userinfo["skills_learned"].append("Shoot")
                userinfo["equip"] = "Simple Bow"
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                await self.bot.say("Great, enjoy your stay!")
                return
            elif answer2 == "2" or answer2 == "paladin":
                userinfo["class"] = "Paladin"
                userinfo["skills_learned"].append("Swing")
                userinfo["equip"] = "Simple Sword"
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                await self.bot.say("Great, enjoy your stay!")
                return
            elif answer2 == "3" or answer2 == "mage":
                userinfo["class"] = "Mage"
                userinfo["skills_learned"].append("Cast")
                userinfo["equip"] = "Simple Staff"
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                await self.bot.say("Great, enjoy your stay!")
                return
            elif answer2 == "4" or answer2 == "thief":
                userinfo["class"] = "Thief"
                userinfo["skills_learned"].append("Stab")
                userinfo["equip"] = "Simple Dagger"
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                await self.bot.say("Great, enjoy your stay!")
                return

    @rpg.command(pass_context = True)
    async def fight(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("{}, Please start your character using `!rpg start`".format(userinfo["name"]))
            return

        if userinfo["health"] <= 0:
            await self.bot.reply("{}, you cannot fight with 0 HP".format(userinfo["name"]))
            return

        if userinfo["location"] == "Golden Temple":
            monsterlist = ["Holy Priest", "Forgotten Spirit", "Unholy Saint"]
        elif userinfo["location"] == "The Forest":
            monsterlist = ["Wolf", "Goblin", "Zombie"]
        elif userinfo["location"] == "Saker Keep":
            monsterlist = ["Draugr", "Stalker", "SoulEater"]

        #IF PLAYER ISNT FIGHTING AN ENEMY, CHOOSE ONE BASED ON LOCATION
        if userinfo["selected_enemy"] == "None":
            debi = random.choice((monsterlist))
            await self.bot.say("{} wanders around {} and finds a {}.\nWould you like to fight it? **Y** or **N**".format(userinfo["name"], userinfo["location"], debi))
            options = ["y", "Y", "yes", "Yes", "n", "N", "No", "no", "!rpg fight"]
            answer1 = await self.check_answer(ctx, options)

            if answer1 == "!rpg fight":
                pass

            if answer1 == "y" or answer1 == "Y" or answer1 == "Yes" or answer1 == "yes":
                userinfo["selected_enemy"] = debi
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)

                if userinfo["selected_enemy"] == "Holy Priest" or userinfo["selected_enemy"] == "Draugr":
                    userinfo["enemyhp"] = random.randint(50, 75)
                    fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                elif userinfo["selected_enemy"] == "Forgotten Spirit" or userinfo["selected_enemy"] == "Stalker":
                    userinfo["enemyhp"] = random.randint(50, 100)
                    fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                elif userinfo["selected_enemy"] == "Unholy Saint" or userinfo["selected_enemy"] == "SoulEater":
                    userinfo["enemyhp"] = random.randint(75, 125)
                    fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)    
                elif userinfo["selected_enemy"] == "Wolf":
                    userinfo["enemyhp"] = random.randint(150, 200)
                    fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo) 
                elif userinfo["selected_enemy"] == "Goblin":
                    userinfo["enemyhp"] = random.randint(125, 150)
                    fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)  
                elif userinfo["selected_enemy"] == "Zombie":
                    userinfo["enemyhp"] = random.randint(175, 225)
                    fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo) 
            elif answer1 == "n" or answer1 == "N" or answer1 == "no" or answer1 == "No":
                await self.bot.say("Okay then.")
                return
        #YOUR DAMAGE BASED ON THE WEAPON YOUR HOLDING
        youdmg = 0
        if userinfo["equip"] == "Simple Dagger":
            youdmg += random.randint(5, 25)
        elif userinfo["equip"] == "Simple Staff":
            youdmg += random.randint(5, 25)
        elif userinfo["equip"] == "Simple Bow":
            youdmg += random.randint(5, 25)
        elif userinfo["equip"] == "Simple Sword":
            youdmg += random.randint(5, 25)
        elif userinfo["equip"] == "Precise Dagger":
            youdmg += random.randint(10, 60)
        elif userinfo["equip"] == "Precise Staff":
            youdmg += random.randint(10, 60)
        elif userinfo["equip"] == "Precise Bow":
            youdmg += random.randint(10, 60)
        elif userinfo["equip"] == "Precise Sword":
            youdmg += random.randint(10, 60)

        #ENEMY DAMAGE BASED ON ENEMY GROUPS
        enemydmg = 0

        if userinfo["selected_enemy"] == "Holy Priest":
            enemydmg += random.randint(0, 10)
            enemygold = random.randint(25, 40)
            goldlost = random.randint(0, 60)
            xpgain = random.randint(5, 10)
        elif userinfo["selected_enemy"] == "Forgotten Spirit":
            enemydmg += random.randint(0, 20)
            enemygold = random.randint(25, 50)
            goldlost = random.randint(0, 70)
            xpgain = random.randint(5, 20)
        elif userinfo["selected_enemy"] == "Unholy Saint":
            enemydmg += random.randint(0, 30)
            enemygold = random.randint(35, 70)
            goldlost = random.randint(0, 80)
            xpgain = random.randint(10, 25)
        elif userinfo["selected_enemy"] == "Draugr":
            enemydmg += random.randint(0, 10)
            enemygold = random.randint(25, 40)
            goldlost = random.randint(0, 60)
            xpgain = random.randint(5, 10)
        elif userinfo["selected_enemy"] == "Stalker":
            enemydmg += random.randint(0, 20)
            enemygold = random.randint(25, 50)
            goldlost = random.randint(0, 70)
            xpgain = random.randint(5, 20)
        elif userinfo["selected_enemy"] == "SoulEater":
            enemydmg += random.randint(0, 30)
            enemygold = random.randint(35, 70)
            goldlost = random.randint(0, 80)
            xpgain = random.randint(10, 25)
        elif userinfo["selected_enemy"] == "Wolf":
            enemydmg += random.randint(10, 40)
            enemygold = random.randint(40, 90)
            goldlost = random.randint(0, 160)
            xpgain = random.randint(10, 30)
        elif userinfo["selected_enemy"] == "Goblin":
            enemydmg += random.randint(10, 60)
            enemygold = random.randint(40, 140)
            goldlost = random.randint(0, 160)
            xpgain = random.randint(10, 30)
        elif userinfo["selected_enemy"] == "Zombie":
            enemydmg += random.randint(10, 40)
            enemygold = random.randint(40, 90)
            goldlost = random.randint(0, 160)
            xpgain = random.randint(10, 30)

        #YOUR SKILL OPTIONS LIST
        show_list = []
        options = ["!rpg fight"]
        if "Swing" in userinfo["skills_learned"]:
            options.append("swing")
            options.append("Swing")
            show_list.append("Swing")
        elif "Stab" in userinfo["skills_learned"]:
            options.append("stab")
            options.append("Stab")
            show_list.append("Stab")
        elif "Shoot" in userinfo["skills_learned"]:
            options.append("shoot")
            options.append("Shoot")
            show_list.append("Shoot")
        elif "Cast" in userinfo["skills_learned"]:
            options.append("cast")
            options.append("Cast")
            show_list.append("Cast")
            
        em = discord.Embed(title="|====[ {} ]====|".format(user.name), description="```diff\n\n- What skill would you like to use:\n+ {}```".format("\n+ ".join(show_list)), color=discord.Color.blue())
        
        await self.bot.say(embed=em)
        
        answer2 = await self.check_answer(ctx, options)

        if answer2 == "!rpg fight":
            return

        #DEFINE WHAT SKILL WE SELECTED
        if answer2 == "cast" or answer2 == "Cast":
            move = "Cast"
        elif answer2 == "shoot" or answer2 == "Shoot":
            move = "Shoot"
        elif answer2 == "swing" or answer2 == "Swing":
            move = "Swing"
        elif answer2 == "stab" or answer2 == "Stab":
            move = "Stab"

        #LETS DEFINE OUR VAR'S
        userhealth = userinfo["health"]
        userhealth1 = userhealth
        userhealth = userhealth - enemydmg
        userlvl = userinfo["lvl"]
        lvlexp = 100 * userlvl

        #LETS DEFINE THE ENEMY'S VAR'S
        enemyhp = userinfo["enemyhp"]
        enemyhp1 = enemyhp
        enemyhp = enemyhp - youdmg
        lootbag = random.randint(1, 10)

        #IF SELECTED A SKILL, FIGHT
        if answer2 in options:
            if enemydmg < 0:
                enemydmg = 0
            if userhealth < 0:
                userhealth = 0
            if enemyhp < 0:
                enemyhp = 0
            em = discord.Embed(description="```diff\n- {} has {} HP\n+ {} has {} HP\n\n- {} hits {} for {} damage\n+ {} uses {} and hits for {} damage\n\n- {} has {} HP left\n+ {} has {} Hp left```".format(userinfo["selected_enemy"], userinfo["enemyhp"], userinfo["name"], userinfo["health"], userinfo["selected_enemy"], userinfo["name"], enemydmg, userinfo["name"], move, youdmg, userinfo["selected_enemy"], enemyhp, userinfo["name"], userhealth), color=discord.Color.red())
            await self.bot.say(embed=em)
            userinfo["health"] = userhealth
            userinfo["enemyhp"] = enemyhp

            if enemyhp <= 0 and userhealth <= 0:
                em = discord.Embed(description="```diff\n- {} has killed you\n- {} lost {} gold.```".format(userinfo["selected_enemy"], userinfo["name"], goldlost), color=discord.Color.red())
                await self.bot.say(embed=em)
                userinfo["gold"] = userinfo["gold"] - goldlost
                if userinfo["gold"] < 0:
                    userinfo["gold"] = 0
                if userinfo["health"] < 0:
                    userinfo["health"] = 0
                userinfo["health"] = 0
                userinfo["selected_enemy"] = "None"
                userinfo["enemieskilled"] = userinfo["enemieskilled"] + 1
                userinfo["deaths"] = userinfo["deaths"] + 1
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)

            elif userhealth <= 0:
                em = discord.Embed(description="```diff\n- {} killed {}\n- {} lost {} gold```".format(userinfo["selected_enemy"], userinfo["name"], userinfo["name"], goldlost), color=discord.Color.red())
                await self.bot.say(embed=em)
                userinfo["gold"] = userinfo["gold"] - goldlost
                if userinfo["gold"] < 0:
                    userinfo["gold"] = 0
                if userinfo["health"] < 0:
                    userinfo["health"] = 0
                userinfo["selected_enemy"] = "None"
                userinfo["deaths"] = userinfo["deaths"] + 1
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)

            elif enemyhp <= 0:
                em = discord.Embed(description="```diff\n+ {} killed the {}\n+ {} gained {} Gold\n+ {} gained {} Exp```".format(userinfo["name"], userinfo["selected_enemy"], userinfo["name"], enemygold, userinfo["name"], xpgain), color=discord.Color.blue())
                await self.bot.say(embed=em)
                userinfo["selected_enemy"] = "None"
                userinfo["gold"] = userinfo["gold"] + enemygold
                userinfo["exp"] = userinfo["exp"] + xpgain
                print(lootbag)
                if lootbag == 6:
                    em = discord.Embed(description="```diff\n+ {} Obtained a Lootbag!```".format(userinfo["name"]), color=discord.Color.blue())
                    await self.bot.say(embed=em)
                    userinfo["lootbag"] = userinfo["lootbag"] + 1
                    fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                userinfo["enemieskilled"] = userinfo["enemieskilled"] + 1
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)

            if userinfo["exp"] >= lvlexp:
                em = discord.Embed(description="```diff\n+ {} gained a level!```".format(userinfo["name"]), color=discord.Color.blue())
                await self.bot.say(embed=em)
                userinfo["lvl"] = userinfo["lvl"] + 1
                userinfo["health"] = 100
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
            fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)

    @rpg.command(pass_context=True)
    async def lootbag(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please create a character using `!rpg menu`")
            return
        if userinfo["lootbag"] == 0:
            em = discord.Embed(description="```diff\n- {}, you don't have any Loot bags!```".format(userinfo["name"]), color=discord.Color.blue())
            await self.bot.say(embed=em)
            return
        else:
            em = discord.Embed(description="```diff\n+ {} starts opening a Lootbag. . .```".format(userinfo["name"]), color=discord.Color.blue())
            await self.bot.say(embed=em)
            await asyncio.sleep(5)
            chance = random.randint(1, 3)
            goldmul = random.randint(10, 30)
            goldgain = goldmul * userinfo["lvl"]
            if chance == 3:
                em = discord.Embed(description="```diff\n+ The Lootbag obtained {} Gold!```".format(goldgain), color=discord.Color.blue())
                await self.bot.say(embed=em)
                userinfo["gold"] = userinfo["gold"] + goldgain
                userinfo["lootbag"] = userinfo["lootbag"] - 1
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
            else:
                em = discord.Embed(description="```diff\n- The Lootbag didn't contain anything!```", color=discord.Color.blue())
                await self.bot.say(embed=em)
                userinfo["lootbag"] = userinfo["lootbag"] - 1
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)

    @rpg.command (pass_context = True)
    async def travel(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `!rpg menu`")
            return
        options = []
        options2 = []
        travel_location = []

        if userinfo["lvl"] > 0:
            options.append("(0) Golden Temple")
            options2.append("0")

            options.append("(1) Saker Keep")
            options2.append("1")

        if userinfo["lvl"] >= 10:
            options.append("(2) The Forest")
            options2.append("2")

        em = discord.Embed(description="<@{}>\n```diff\n+ Where would you like to travel?\n- Type a location number in the chat.\n+ {}```".format(user.id, "\n+ ".join(options)), color=discord.Color.blue())
        await self.bot.say(embed=em)

        answer1 = await self.check_answer(ctx, options2)

        if answer1 == "0":
            if userinfo["location"] == "Golden Temple":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(user.id, userinfo["location"]), color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            else:
                location_name = "Golden Temple"
                userinfo["location"] = "Golden Temple"

        elif answer1 == "1":
            if userinfo["location"] == "Saker Keep":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(user.id, userinfo["location"]), color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            else:
                location_name = "Saker Keep"
                userinfo["location"] = "Saker Keep"

        elif answer1 == "2":
            if userinfo["location"] == "The Forest":
                em = discord.Embed(description="<@{}>\n```diff\n- You're already at {}!```".format(user.id, userinfo["location"]), color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            else:
                location_name = "The Forest"
                userinfo["location"] = "The Forest"

        em = discord.Embed(description="<@{}>\n```diff\n+ Traveling to {}...```".format(user.id, location_name), color=discord.Color.red())
        await self.bot.say(embed=em)
        await asyncio.sleep(3)
        userinfo["location"] = location_name
        fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
        await self.bot.say("You have arrived at {}".format(location_name))
        em = discord.Embed(description="<@{}>\n```diff\n+ You have arrived at {}```".format(user.id, location_name), color=discord.Color.red())
        await self.bot.say(embed=em)

    @rpg.command(pass_context = True)
    async def inv(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `!rpg menu`")
            return
        em = discord.Embed(description="```diff\n!======== [{}'s Inventory] ========!\n\n!==== [Supplies] ====!\n+ Gold : {}\n+ Wood : {}\n+ Stone : {}\n+ Metal : {}\n\n!===== [Items] =====!\n+ Keys : {}\n+ Loot Bags : {}\n+ Minor HP Potions : {}\n+ {}```".format(userinfo["name"], userinfo["gold"], userinfo["wood"], userinfo["stone"], userinfo["metal"], userinfo["keys"], userinfo["lootbag"], userinfo["hp_potions"], "\n+ ".join(userinfo["inventory"])), color=discord.Color.blue())
        await self.bot.say(embed=em)

    @rpg.command(pass_context = True)
    async def stats(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `!rpg menu`")
            return
        maxexp = 100 * userinfo["lvl"]
        em = discord.Embed(description="```diff\n!======== [{}'s Stats] ========!\n+ Name : {}\n+ Title : {}\n+ Race : {}\n+ Class : {}\n\n+ Level : {} | Exp : ({}/{})\n+ Health : ({}/100)\n+ Stamina : {}\n+ Mana : {}\n\n!===== [Equipment] =====!\n+ Weapon : {}\n+ Wearing : {}\n\n+ Killed : {} Enemies\n+ Died : {} Times```".format(userinfo["name"], userinfo["name"], userinfo["title"], userinfo["race"], userinfo["class"], userinfo["lvl"], userinfo["exp"], maxexp, userinfo["health"], userinfo["stamina"], userinfo["mana"], userinfo["equip"], userinfo["wearing"], userinfo["enemieskilled"], userinfo["deaths"]), color=discord.Color.blue())
        await self.bot.say(embed=em)

    @rpg.command(pass_context = True)
    async def equip(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `!rpg menu`")
            return
        choices = []
        inv_list = [i for i in userinfo["inventory"]]
        if len(inv_list) == 0:
            em = discord.Embed(description="```diff\n- You don't have anything else to equip!```", color=discord.Color.red())
            await self.bot.say(embed=em)
        else:
            choices.append(inv_list)
            em = discord.Embed(description="```diff\n+ What would you like to equip?\n- Note this is Uppercase and Lowercase sensitive.\n{}```".format("\n".join(inv_list)), color=discord.Color.blue())
            await self.bot.say(embed=em)
            answer1 = await self.check_answer(ctx, inv_list)
            await self.bot.say("You equiped the {}!".format(answer1))
            em = discord.Embed(description="```diff\n+ You equip the {}!```".format(answer1), color=discord.Color.blue())
            await self.bot.say(embed=em)
            userinfo["inventory"].append(userinfo["equip"])
            userinfo["equip"] = "None"
            userinfo["equip"] = answer1
            userinfo["inventory"].remove(answer1)
            fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)

    @rpg.group(pass_context = True)
    async def buy(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `!rpg menu`")
            return
        weapons_list = ["hp","Hp", "Precise sword", "Precise sword", "Precise bow", "Precise bow", "Precise dagger", "Precise dagger", "Precise staff", "Precise staff"]
        if ctx.invoked_subcommand is None:
            em = discord.Embed(description="```>buy item_name\n\nNote: It must all be lowercase.```", color=discord.Color.blue())
            await self.bot.say(embed=em)

    @buy.command(pass_context=True)
    async def hp(self, ctx, *, ammount : int):
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        Sum = ammount * 30

        if ammount == None:
            ammount = 1

        if userinfo["gold"] < Sum:
            needed = Sum - userinfo["gold"]
            em = discord.Embed(description="```diff\n- You need {} more gold for {} potion(s)```".format(needed, ammount), color=discord.Color.red())
            await self.bot.say(embed=em)
        else:   
            userinfo["gold"] = userinfo["gold"] - Sum
            userinfo["hp_potions"] = userinfo["hp_potions"] + int(ammount)
            fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n+ You bought {} potion(s) for {} Gold```".format(ammount, Sum), color=discord.Color.blue())
            await self.bot.say(embed=em)

    @buy.command(pass_context=True)
    async def item(self, ctx, *, item):
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if item == "Precise sword":
            if not userinfo["class"] == "Paladin":
                em = discord.Embed(description="```diff\n- You need to be a Paladin to buy this item.```", color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="```diff\n- You need {} more Gold to buy this item.```".format(value), color=discord.Color.red())
                await self.bot.say(embed=em)
            else:
                cost = 1000
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append("Precise Sword")
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                em = discord.Embed(description="```diff\n+ You bought the item for {} Gold.```".format(cost), color=discord.Color.blue())
                await self.bot.say(embed=em)

        elif item == "Precise dagger":
            if not userinfo["class"] == "Thief":
                em = discord.Embed(description="```diff\n- You need to be a Thief to buy this item.```", color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="```diff\n- You need {} more Gold to buy this item.```".format(value), color=discord.Color.red())
                await self.bot.say(embed=em)
            else:
                cost = 1000
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append("Precise Dagger")
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                em = discord.Embed(description="```diff\n+ You bought the item for {} Gold.```".format(cost), color=discord.Color.blue())
                await self.bot.say(embed=em)

        elif item == "Precise bow":
            if not userinfo["class"] == "Ranger":
                em = discord.Embed(description="```diff\n- You need to be an Ranger to buy this item.```", color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="```diff\n- You need {} more Gold to buy this item.```".format(value), color=discord.Color.red())
                await self.bot.say(embed=em)
            else:
                cost = 1000
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append("Precise Bow")
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                em = discord.Embed(description="```diff\n+ You bought the item for {} Gold.```".format(cost), color=discord.Color.blue())
                await self.bot.say(embed=em)

        elif item == "Precise staff":
            if not userinfo["class"] == "Mage":
                em = discord.Embed(description="```diff\n- You need to be a Mage to buy this item.```", color=discord.Color.red())
                await self.bot.say(embed=em)
                return
            cost = 1000
            value = cost - userinfo["gold"]
            if userinfo["gold"] < cost:
                em = discord.Embed(description="```diff\n- You need {} more Gold to buy this item.```".format(value), color=discord.Color.red())
                await self.bot.say(embed=em)
            else:
                cost = 1000
                userinfo["gold"] = userinfo["gold"] - cost
                userinfo["inventory"].append("Precise Staff")
                fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
                em = discord.Embed(description="```diff\n+ You bought the item for {} Gold.```".format(cost), color=discord.Color.blue())
                await self.bot.say(embed=em)
        else:
            em = discord.Embed(description="```diff\n- You have requested to buy an invalid item.\n\n+ To see the list of the items, type >items```", color=discord.Color.red())
            await self.bot.say(embed=em)

    @rpg.command(pass_context=True)
    async def items(self, ctx, *, Class):
        user = ctx.message.author
        if Class == "Mage" or Class == "mage":
            em = discord.Embed(description="```diff\n+ Item list for the Mage Class.```\n\n1) Precise Staff - [1,000 Gold]", color=discord.Color.blue())
            await self.bot.say(embed=em)
        elif Class == "Paladin" or Class == "paladin":
            em = discord.Embed(description="```diff\n+ Item list for the Paladin Class.```\n\n1) Precise Sword - [1,000 Gold]", color=discord.Color.blue())
            await self.bot.say(embed=em)
        elif Class == "Thief" or Class == "thief":
            em = discord.Embed(description="```diff\n+ Item list for the Thief Class.```\n\n1) Precise Dagger - [1,000 Gold]", color=discord.Color.blue())
            await self.bot.say(embed=em)
        elif Class == "Ranger" or Class == "ranger":
            em = discord.Embed(description="```diff\n+ Item list for the Ranger Class.```\n\n1) Precise Bow - [1,000 Gold]", color=discord.Color.blue())
            await self.bot.say(embed=em)
        else:
            em = discord.Embed(description="```diff\n- That is not a valid Class.```", color=discord.Color.red())
            await self.bot.say(embed=em)

    @rpg.command(pass_context = True)
    async def heal(self, ctx):
        user = ctx.message.author
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `!rpg menu`")
            return
        if userinfo["hp_potions"] > 0:
            gain = random.randint(90, 100)
            userinfo["health"] = userinfo["health"] + gain
            if userinfo["health"] > 100:
                userinfo["health"] = 100
            userinfo["hp_potions"] = userinfo["hp_potions"] - 1
            fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n- You use a Minor Health Potion\n+ {} HP```".format(gain), color=discord.Color.red())
            await self.bot.say(embed=em)
        else:
            em = discord.Embed(description="```diff\n- You don't have any health potions!```", color=discord.Color.red())
            await self.bot.say(embed=em)


    @rpg.command(pass_context=True)
    async def daily(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        goldget = random.randint(500, 1000)
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `!rpg menu`")
            return
        curr_time = time.time()
        delta = float(curr_time) - float(userinfo["daily_block"])

        if delta >= 86400.0 and delta>0:
            if userinfo["class"] == "None" and userinfo["race"] == "None":
                await self.bot.reply("Please start your player using `!rpg menu`")
                return
            userinfo["gold"] += goldget
            userinfo["daily_block"] = curr_time
            fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n+ You received your daily gold!\n+ {}```".format(goldget), color=discord.Color.blue())
            await self.bot.say(embed=em)
        else:
            # calculate time left
            seconds = 86400 - delta
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            em = discord.Embed(description="```diff\n- You can't claim your daily reward yet!\n\n- Time left:\n- {} Hours, {} Minutes, and {} Seconds```".format(int(h), int(m), int(s)), color=discord.Color.red())
            await self.bot.say(embed=em)

    @rpg.command(pass_context=True)
    async def rest(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        HPget = random.randint(10, 40)
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `!rpg menu`")
            return
        curr_time = time.time()
        delta = float(curr_time) - float(userinfo["rest_block"])

        if delta >= 120.0 and delta>0:
            if userinfo["class"] == "None" and userinfo["race"] == "None":
                await self.bot.reply("Please start your player using `!rpg menu`")
                return
            userinfo["health"] = userinfo["health"] + HPget
            if userinfo["health"] > 100:
                userinfo["health"] = 100
            userinfo["rest_block"] = curr_time
            fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n+ You gained {} HP for resting!```".format(HPget), color=discord.Color.blue())
            await self.bot.say(embed=em)
        else:
            # calculate time left
            seconds = 120 - delta
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            em = discord.Embed(description="```diff\n- Your not tired!\n\n- Time left:\n- {} Hours, {} Minutes, and {} Seconds```".format(int(h), int(m), int(s)), color=discord.Color.red())
            await self.bot.say(embed=em)

    @rpg.command(pass_context=True)
    async def mine(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        mined_metal = random.randint(1, 10)
        mined_rock = random.randint(1, 10)
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `!rpg menu`")
            return
        curr_time = time.time()
        delta = float(curr_time) - float(userinfo["mine_block"])

        if delta >= 600.0 and delta>0:
            if userinfo["class"] == "None" and userinfo["race"] == "None":
                await self.bot.reply("Please start your player using `!rpg menu`")
                return
            userinfo["metal"] = userinfo["metal"] + mined_metal
            userinfo["stone"] = userinfo["stone"] + mined_rock
            userinfo["mine_block"] = curr_time
            fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n+ {} mined a Rock!\n+ {} Metal\n+ {} Stone```".format(userinfo["name"], mined_metal, mined_rock), color=discord.Color.blue())
            await self.bot.say(embed=em)
        else:
            # calculate time left
            seconds = 600 - delta
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            em = discord.Embed(description="```diff\n- You cannot mine yet!\n\n- Time left:\n- {} Hours, {} Minutes, and {} Seconds```".format(int(h), int(m), int(s)), color=discord.Color.red())
            await self.bot.say(embed=em)

    @rpg.command(pass_context=True)
    async def chop(self, ctx):
        channel = ctx.message.channel
        user = ctx.message.author
        chopped = random.randint(1, 10)
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")
        if userinfo["race"] and userinfo["class"] == "None":
            await self.bot.say("Please start your character using `!rpg menu`")
            return
        curr_time = time.time()
        delta = float(curr_time) - float(userinfo["chop_block"])

        if delta >= 600.0 and delta>0:
            if userinfo["class"] == "None" and userinfo["race"] == "None":
                await self.bot.reply("Please start your player using `!rpg menu`")
                return
            userinfo["wood"] = userinfo["wood"] + chopped
            userinfo["chop_block"] = curr_time
            fileIO("data/rpg/players/{}/info.json".format(user.id), "save", userinfo)
            em = discord.Embed(description="```diff\n+ You chopped a Tree!\n+ {} Wood```".format(chopped), color=discord.Color.blue())
            await self.bot.say(embed=em)
        else:
            # calculate time left
            seconds = 600 - delta
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            em = discord.Embed(description="```diff\n- You cannot chop yet!\n\n- Time left:\n- {} Hours, {} Minutes, and {} Seconds```".format(int(h), int(m), int(s)), color=discord.Color.red())
            await self.bot.say(embed=em)

    def _name(self, user, max_length):
        if user.name == user.display_name:
            return user.name
        else:
            return "{} ({})".format(user.name, self._truncate_text(user.display_name, max_length - len(user.name) - 3), max_length)

    async def on_message(self, message):
        if message.content.startswith('!rpg'):
            await self.bot.delete_message(message)
        await self._handle_on_message(message)

    async def _handle_on_message(self, message):
        text = message.content
        channel = message.channel
        server = message.server
        user = message.author
        # creates user if doesn't exist, bots are not logged.
        await self._create_user(user, server)
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")

    # handles user creation.
    async def _create_user(self, user, server):
        if not os.path.exists("data/rpg/players/{}".format(user.id)):
            os.makedirs("data/rpg/players/{}".format(user.id))
            new_account = {
                "name": user.name,
                "race": "None",
                "class": "None",
                "health": 100,
                "enemyhp": 50,
                "enemylvl": 0,
                "lvl": 0,
                "gold": 0,
                "wood": 0,
                "metal": 0,
                "stone": 0,
                "enemieskilled": 0,
                "selected_enemy": "None",
                "deaths": 0,
                "exp": 0,
                "lootbag": 0,
                "wearing": "None",
                "defense": 0,
                "guild": "None",
                "inguild": "None",
                "skills_learned": [],
                "inventory" : [],
                "equip": "None",
                "title": "None",
                "wincry": "None",
                "losecry": "None",
                "location": "Golden Temple",
                "roaming": "False",
                "pet": "None",
                "mana": 100,
                "stamina": 100,
                "craftable": [],
                "daily_block": 0,
                "rest_block": 0,
                "fight_block": 0,
                "traveling_block": 0,
                "hp_potions": 0,
                "keys": 0,
                "mine_block": 0,
                "chop_block": 0,
                "in_dungeon": "False",
                "dungeon_enemy": "None",
                "duneon_enemy_hp": 0,
                "in_party": [],
                "thirst": 0,
                "hunger": 0,
                "tiredness": 0
            }
            fileIO("data/rpg/players/{}/info.json".format(user.id), "save", new_account)
        userinfo = fileIO("data/rpg/players/{}/info.json".format(user.id), "load")

def check_folders():
    if not os.path.exists("data/rpg"):
        print("Creating data/rpg folder...")
        os.makedirs("data/rpg")

    if not os.path.exists("data/rpg/players"):
        print("Creating data/rpg/players folder...")
        os.makedirs("data/rpg/players")
        transfer_info()

def transfer_info():
    players = fileIO("data/rpg/players.json", "load")
    for user_id in players:
        os.makedirs("data/rpg/players/{}".format(user_id))
        # create info.json
        f = "data/rpg/players/{}/info.json".format(user_id)
        if not fileIO(f, "check"):
            fileIO(f, "save", players[user_id])

def setup(bot):
    check_folders()

    n = RPG(bot)
    bot.add_listener(n.on_message,"on_message")
    bot.add_cog(n)