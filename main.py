import discord
import logging
import os
import json
import aiomysql
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands

with open("config.json",'r') as configjsonFile:
    configData=json.load(configjsonFile)
    TOKEN=configData["DISCORD_TOKEN"]

times_used = 0

activity = discord.Activity(type = discord.ActivityType.watching, name="Leaderboards & Points")
client = commands.Bot(command_prefix='&',activity=activity,strip_after_prefix = True,owner_id = 315342835283001344)
client.remove_command("help")



intents = discord.Intents.default()
intents.members = True

async def create_pool():
    client.db = await aiomysql.connect(host='173.249.9.178', port=5023,user='AxomDB', password='ASHISHaxomdb#2022', db='AXOMDB')
    print("connected to db")
    cur = await client.db.cursor()
client.loop.create_task(create_pool())

@client.command()
@commands.is_owner()
async def loadcog(ctx,extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.is_owner()
async def unloadcog(ctx,extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def test(ctx, arg):
    await ctx.send(arg)

client.run(TOKEN)