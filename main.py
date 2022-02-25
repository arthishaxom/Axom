import discord
import os
import json
import asyncpg
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
    # client.db = await asyncpg.connect(host='containers-us-west-29.railway.app', port=7183,user='postgres', password='C81BI8wU7QHzR5mXTvMZ', db='railway')
    client.db = await asyncpg.connect(host='bunbhl3ahvcmset3bk2e-postgresql.services.clever-cloud.com', port=5432,user='uooqkec81x9lbjrz6noi', password='dMlCwvxEyVASRyAsRFuB', database='bunbhl3ahvcmset3bk2e')
    print("connected to db")


client.loop.run_until_complete(create_pool())


@client.command()
@commands.is_owner()
async def loadcog(ctx,extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("DONE")

@client.command()
@commands.is_owner()
async def unloadcog(ctx,extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("DONE")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def test(ctx, arg):
    msg = await ctx.send(arg)
    def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
    await msg.add_reaction("✅")

client.run(TOKEN)