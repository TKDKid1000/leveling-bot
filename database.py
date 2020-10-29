import discord
from discord.utils import get
from discord.ext import commands
import asyncio
import pickle
bot = commands.Bot(command_prefix=".")

load_file = open('C:\\Users\\rhone\\OneDrive\\Desktop\\database.dat', 'rb')
people = pickle.load(load_file)
load_file.close()

@bot.event()
async def on_member_join(member):
    mname = member.get(name)
    mtag = member.get(discriminator)
    people[mname] = {"name" : mname, "tag" : mtag, "level" : "1"}
    print(people)

people = {
    "joe" : {"name" : "joe", "tag" : "#0001", "level" : "10"},
    "bob" : {"name" : "bob", "tag" : "#0002", "level" : "5"},
    "alex" : {"name" : "alex", "tag" : "#0003", "level" : "7"}
}

@bot.command()
async def database(ctx):
    await ctx.send("Check console")
    for person in people:
        person = people[person]
        print(person["name"] + person["tag"] + " is level " + person["level"]) 
bot.run("NzQwMzc1MzA0NTcyMzcwOTc0.XyoGPA.j6Ln1Z5HA7VxKpi_vM7Q7i3f2NA")