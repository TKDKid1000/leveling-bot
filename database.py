import discord
from discord.utils import get
from discord.ext import commands
import asyncio
import json
import os
import random
# define bot
bot = commands.Bot(command_prefix="!")
bot.remove_command("help")

# define bot settings from settings.txt
f = open(os.path.dirname(os.path.abspath(__file__)) + '\\settings.txt')
settings = f.read()
settings = settings.split("\n")
f.close()
# loop through every setting and define variables for them
for setting in settings:
    if setting.startswith("token: "):
        token = setting.replace("token: ", "")
        print("Token: " + token)
    if setting.startswith("maxearn: "):
        maxearn = int(setting.replace("maxearn: ", ""))
        print("Max earn: " + str(maxearn))
    if setting.startswith("levelup: "):
        levelup = int(setting.replace("levelup: ", ""))
        print("Levelup: " + str(levelup))


@bot.event
async def on_ready():
    print("ready")

@bot.command()
async def levels(ctx):
    toplist = []
    with open(os.path.dirname(os.path.abspath(__file__)) + '\\database.json') as f:
        people = json.load(f)
        for person in people:
            person = people[person]
            toplist.append({person["name"] + "#" + person["tag"] : str(person["level"]*levelup+person["xp"])})
        toplist = sorted(toplist, key=lambda x: list(x.values())[0], reverse=True)
        top1 = str(toplist[0]).replace("{", "").replace("}", "").replace("'", "").replace(":", "")
        top2 = str(toplist[1]).replace("{", "").replace("}", "").replace("'", "").replace(":", "")
        top3 = str(toplist[2]).replace("{", "").replace("}", "").replace("'", "").replace(":", "")
        top4 = str(toplist[3]).replace("{", "").replace("}", "").replace("'", "").replace(":", "")
        top5 = str(toplist[4]).replace("{", "").replace("}", "").replace("'", "").replace(":", "")
        embed=discord.Embed(title="Leaderboard", description=f'''The top 5 scoring members!
        #1 {top1}
        #2 {top2}
        #3 {top3}
        #4 {top4}
        #5 {top5}''')
        await ctx.send(embed=embed)
        


@bot.command()
@commands.has_permissions(administrator=True)
async def xp(ctx, cmd=None, member: discord.Member=None, arg2=None):
    if cmd == None:
        await ctx.send('''Xp Commands:
        xp set <player> <amount> set a players xp
        xp level <player> <amount> set a players level''')
    else:
        with open(os.path.dirname(os.path.abspath(__file__)) + '\\database.json') as f:
            people = json.load(f)
            name = str(member.id)
            person = people[name]
            if cmd == "set":
                person["xp"] = int(arg2)
                await ctx.send(f'''Set {member.mention}'s xp to {arg2}''')
                with open(os.path.dirname(os.path.abspath(__file__)) + '\\database.json', 'w') as json_file:
                    json.dump(people, json_file)
            if cmd == "level":
                person["level"] = int(arg2)
                await ctx.send(f'''Set {member.mention}'s level to {arg2}''')
                with open(os.path.dirname(os.path.abspath(__file__)) + '\\database.json', 'w') as json_file:
                    json.dump(people, json_file)


@bot.command()
async def rank(ctx, target: discord.Member = None):
    if target == None:
        with open(os.path.dirname(os.path.abspath(__file__)) + '\\database.json') as f:
            people = json.load(f)
            person = people[str(ctx.author.id)]
        embed=discord.Embed(title=f"**Rank For {ctx.author}**", description=f'''Level: {person["level"]} Xp: {person["xp"]}/{levelup}''', color=0x00e4f5)
        await ctx.send(embed=embed)
    else:
        with open(os.path.dirname(os.path.abspath(__file__)) + '\\database.json') as f:
            people = json.load(f)
            person = people[str(target.id)]
        embed=discord.Embed(title=f"**Rank For {target}**", description=f'''Level: {person["level"]} Xp: {person["xp"]}/{levelup}''', color=0x00e4f5)
        await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    # dont respond to bot
    if message.author == bot.user:
        return
    # initially open file or usage
    with open(os.path.dirname(os.path.abspath(__file__)) + '\\database.json') as f:
        people = json.load(f)
        # define person
        name = str(message.author.id)
        # check if they already exist
        if name in people:
            person = people[name]
            # update name/tag
            person["name"] = message.author.name
            person["tag"] = message.author.discriminator
            # edit xp
            earned = random.randint(1, maxearn)
            person["xp"] = person["xp"]+earned
            # ignore when checking level
            if message.content.startswith("!rank"):
                person["xp"] = person["xp"]-earned
            # add a level if they reached levelup xp
            if person["xp"] > levelup:
                person["level"] = person["level"]+1
                person["xp"] = 0
                embed=discord.Embed(title=f"**Level Up!**", description=f'''Congrats {message.author}, you reached level {person["level"]}!''', color=0x00e4f5)
                await message.channel.send(embed=embed)
            # save file
            with open(os.path.dirname(os.path.abspath(__file__)) + '\\database.json', 'w') as json_file:
                json.dump(people, json_file)
        else:
            people[name] = {"name" : message.author.name, "tag" : message.author.discriminator, "xp" : 1, "level" : 1}
            with open(os.path.dirname(os.path.abspath(__file__)) + '\\database.json', 'w') as json_file:
                json.dump(people, json_file)
            print("added you to the database, here is the info")
            person = people[name]
            print(f'''{person}''')
    await bot.process_commands(message)

bot.run(token)
