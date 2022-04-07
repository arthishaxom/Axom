import discord
import os
import json
import asyncpg
from discord.ext import commands
from discord import app_commands
import jishaku
import asyncio
import typing
from Utilities.BotColoursInfo import BotColours

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

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(
#     filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter(
#     '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)
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

os.environ["JISHAKU_NO_UNDERSCORE"] = "t"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "t"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "t"
os.environ["JISHAKU_HIDE"] = "t"


@client.command()
@commands.is_owner()
async def sync(ctx, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~"]] = None) -> None:
    if not guilds:
        if spec == "~":
            fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        else:
            fmt = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(fmt)} commands {'globally' if spec is not None else 'to the current guild.'}"
        )
        return

    assert guilds is not None
    fmt = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            fmt += 1

    await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds.")
asyncio.run(main())
