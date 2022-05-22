import discord
from discord.ext import commands
import traceback


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

    @commands.command(name='createtable', aliases=["ct", "createt"], case_insensitive=True)
    @commands.is_owner()
    async def createtable(self, ctx):
        async with self.client.pool.acquire() as connection:
            # create a transaction for that connection
            async with connection.transaction():
                for i in range(10):
                    await connection.execute(f'''CREATE TABLE IF NOT EXISTS Points{i+1}(ServerID BIGINT,TeamNames VARCHAR(50),WWCD{i+1} SMALLINT,Position{i+1} SMALLINT,Kills{i+1} SMALLINT,Total{i+1} SMALLINT)''')
                    await connection.execute(f'''CREATE TABLE IF NOT EXISTS SaveInfo(ServerID BIGINT,TableNum SMALLINT,Slotlist VARCHAR(1000),LeftMatches SMALLINT, MatchPos VARCHAR(1000), MatchCd VARCHAR(1000))''')

        await ctx.send("Created Table")

    @commands.command(name='deletetable', aliases=["dt", "deletet"], case_insensitive=True)
    @commands.is_owner()
    async def deletetable(self, ctx):
        async with self.client.pool.acquire() as connection:
            # create a transaction for that connection
            async with connection.transaction():
                for i in range(10):
                    await connection.execute(f'''DROP TABLE IF EXISTS Points{i+1}''')
                    await connection.execute(f'''DROP TABLE IF EXISTS SaveInfo''')
                # await connection.execute(f'''DROP TABLE IF EXISTS Points''')
        await ctx.send("Deleted Table")

    @commands.command(name='cleartable', aliases=["cleart"], case_insensitive=True)
    @commands.is_owner()
    async def cleartable(self, ctx, table, serverid: int):
        await ctx.send(fr'''
async with bot.pool.acquire() as connection:
    async with connection.transaction():
        await connection.execute("DELETE FROM {table} WHERE ServerID = {serverid}")

''')

    @commands.command(name='gettable', aliases=["gt", "gett"], case_insensitive=True)
    @commands.is_owner()
    async def gettable(self, ctx, NoOfMatches: int = 0):

        PositionSyntax = "Position1"
        WwcdSyntax = "WWCD1"
        KillsSyntax = "Kills1"
        TotalSyntax = "Total1"
        JoinSyntax = ""
        TableNumber = 0
        for MatchNumber in range(1, NoOfMatches + 1):
            PositionSyntax += f" + Position{MatchNumber+1}"
            WwcdSyntax += f" + WWCD{MatchNumber+1}"
            KillsSyntax += f" + Kills{MatchNumber+1}"
            TotalSyntax += f" + Total{MatchNumber+1}"
            JoinSyntax += f" INNER JOIN Points{MatchNumber+1} ON Points1.ServerID = Points{MatchNumber+1}.ServerID AND Points1.TeamNames = Points{MatchNumber+1}.TeamNames"
        PositionSyntax += f" AS TotalPosition"
        WwcdSyntax += f" AS TotalWWCD"
        KillsSyntax += f" AS TotalKills"
        TotalSyntax += f" AS TotalPoints"
        # if NoOfMatches > 1:
        #     JoinSyntax += f" USING (ServerID)"
        await ctx.send(f'''SELECT Points1.TeamNames,{PositionSyntax},{WwcdSyntax},{KillsSyntax},{TotalSyntax} FROM Points1{JoinSyntax} ORDER BY TotalPoints DESC, TotalWWCD DESC, TotalPosition DESC, TotalKills DESC LIMIT 20''')
        async with self.client.pool.acquire() as connection:
            # create a transaction for that connection
            async with connection.transaction():
                # await connection.execute(f'''DROP TABLE IF EXISTS Points''')
                AllPoints = await connection.fetch(f'''SELECT Points1.TeamNames,{PositionSyntax},{WwcdSyntax},{KillsSyntax},{TotalSyntax} FROM Points1{JoinSyntax} ORDER BY TotalPoints DESC, TotalWWCD DESC, TotalPosition DESC, TotalKills DESC LIMIT 20''')
        await ctx.send(AllPoints)


async def setup(client):
    await client.add_cog(noneed(client))
