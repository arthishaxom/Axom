import discord
from discord.ext import commands
import os
import json
import asyncpg
import jishaku
import asyncio

with open("config.json", 'r') as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["DISCORD_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

times_used = 0
activity = discord.Activity(
    type=discord.ActivityType.watching, name="Leaderboards & Points")
client = commands.Bot(command_prefix='&', activity=activity,
                      strip_after_prefix=True, owner_id=315342835283001344, intents=intents)
client.remove_command("help")


# async def create_pool():
#     # client.db = await asyncpg.connect(host='containers-us-west-29.railway.app', port=7183,user='postgres', password='C81BI8wU7QHzR5mXTvMZ', db='railway')
#     client.db = await asyncpg.connect(host='containers-us-west-29.railway.app', port=7183,user='postgres', password='C81BI8wU7QHzR5mXTvMZ', database='railway')
#     print("connected to db")


# client.loop.run_until_complete(create_pool())

async def main():
    async with client:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await client.load_extension(f'cogs.{filename[:-3]}')
        await client.load_extension('jishaku')
        await client.start(TOKEN)


@client.command()
@commands.is_owner()
async def loadcog(ctx, extension):
    await client.load_extension(f'cogs.{extension}')
    await ctx.send("DONE")


@client.command()
@commands.is_owner()
async def unloadcog(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await ctx.send("DONE")

os.environ["JISHAKU_NO_UNDERSCORE"] = "t"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "t"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "t"


@client.command()
async def test(ctx, arg):
    msg = await ctx.send(arg)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    await msg.add_reaction("✅")

asyncio.run(main())
