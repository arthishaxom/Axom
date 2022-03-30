import discord
from discord.ext import commands

class noneed(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(ctx, arg):
        msg = await ctx.send(arg)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        await msg.add_reaction("✅")

    @commands.command()
    @commands.is_owner()
    async def loadcog(self, ctx, extension):
        await self.client.load_extension(f'cogs.{extension}')
        await ctx.send("DONE")

    @commands.command()
    @commands.is_owner()
    async def unloadcog(self, ctx, extension):
        await self.client.unload_extension(f'cogs.{extension}')
        await ctx.send("DONE")


async def setup(client):
    await client.add_cog(noneed(client))
