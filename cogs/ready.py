from discord.ui import Button
import discord
from discord import channel
from discord.ext import commands, tasks
import re

class Ready(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.db_check.start()
        except:
            pass
        print("SAB SAHI HAI BIDU")

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        embed = discord.Embed(title = "Thanks For Inviting Axom!",description = "`AXOM` Is A New Bot And Is Open For Suggestions, Kindly Join This Server If You Need Help/Have Any Query : \n> [Axom Support](https://discord.gg/uW7WXxBtBW)")
        try:
            bot_entry = await guild.audit_logs(action = discord.AuditLogAction.bot_add).flatten()
            await bot_entry[0].user.send(embed = embed)
        except:
            return

    @tasks.loop(hours = 7)
    async def db_check(self):
        channel = self.client.get_channel(918849166371868712)
        await channel.send("Test Successful!")
        async with self.client.db.cursor() as cur:
            await cur.execute("CREATE TABLE IF NOT EXISTS test1(team1 VARCHAR(255))")
            await cur.execute("DROP TABLE IF EXISTS test1")

    @commands.Cog.listener()
    async def on_message(self,message: discord.Message) -> None:
        if re.fullmatch(rf"<@!?{self.client.user.id}>",message.content):
            await message.channel.send(f"My prefix is `&`")
            return


        


def setup(client):
    client.add_cog(Ready(client))