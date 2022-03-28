from discord import ui
from discord.ext import menus
import discord
from discord.ext import commands
import psutil
import datetime
import time


class MySource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        embed = discord.Embed(
            description=f"{entries}",
            color=discord.Colour.gold())
        embed.set_footer(text=f"Requested by {menu.ctx.author}")
        return embed


class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None

    async def start(self, ctx, *, channel=None, wait=False):
        # We wont be using wait/channel, you can implement them yourself. This is to match the MenuPages signature.
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        """This method calls ListPageSource.format_page class"""
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        """Only allow the author that invoke the command to be able to use the interaction"""
        return interaction.user == self.ctx.author

    # This is extremely similar to Custom MenuPages(I will not explain these)
    @ui.button(emoji='<:before_fast_check:754948796139569224>', style=discord.ButtonStyle.blurple)
    async def first_page(self, button, interaction):
        await self.show_page(0)

    @ui.button(emoji='<:before_check:754948796487565332>', style=discord.ButtonStyle.blurple)
    async def before_page(self, button, interaction):
        await self.show_checked_page(self.current_page - 1)

    @ui.button(emoji='<:stop_check:754948796365930517>', style=discord.ButtonStyle.blurple)
    async def stop_page(self, button, interaction):
        self.stop()

    @ui.button(emoji='<:next_check:754948796361736213>', style=discord.ButtonStyle.blurple)
    async def next_page(self, button, interaction):
        await self.show_checked_page(self.current_page + 1)

    @ui.button(emoji='<:next_fast_check:754948796391227442>', style=discord.ButtonStyle.blurple)
    async def last_page(self, button, interaction):
        await self.show_page(self._source.get_max_pages() - 1)


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @commands.command(name='serverlist', aliases=['servers', 'slist'])
    @commands.is_owner()
    async def serverlist(self, ctx):
        serverlist = []
        i = 0
        for guild in self.client.guilds:
            i += 1
            e = f"` {str(i)} ` - {guild.name} : `{guild.id}`"
            serverlist.append(e)

        total_servers = len(serverlist)
        serverlist = [serverlist[i:i+10] for i in range(0, total_servers, 10)]

        serverlist_strings = []
        for i in range(len(serverlist)):
            server_strings = "\n".join(serverlist[i])
            serverlist_strings.append(server_strings)

        formatter = MySource(serverlist_strings, per_page=1)
        menu = MyMenuPages(formatter)
        await menu.start(ctx)

    @commands.command(help="Shows the bot's latency")
    async def ping(self, ctx):
        await ctx.send(f"My Ping : `{round(self.client.latency*1000)}ms` <:icon_ping:938972151510360125>\nThis Means Alive...Right?")

    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx, guild_id):
        await self.client.get_guild(int(guild_id)).leave()
        await ctx.send(f"I left: {guild_id}")

    @commands.command(name='botinfo', pass_context=True, case_insensitive=True, aliases=['bi'], help='Shows bot info')
    async def botinfo(self, ctx):
        memory_usage = psutil.virtual_memory()[3] >> 20
        memory_total = psutil.virtual_memory()[0] >> 20
        cpu_usage = psutil.cpu_percent(1)

        member_count = sum(guild.member_count for guild in self.client.guilds)

        embed = discord.Embed(
            title="AXOM Stats", description="Emoji Credits | [Icons Server](https://discord.gg/3aHwMpsDgS)", color=discord.Colour.gold())
        embed.add_field(name="**<:icon_servers:947357898143588352> __Servers Info__**", value=f'''
Total Servers : {len(self.client.guilds)}
Total Users : {member_count}        
''')
        embed.add_field(name="**<:icon_system:947358360859189251> __System Stats__**", value=f'''
CPU : {cpu_usage}% Used
RAM : {memory_usage}/{memory_total} Used
''')

        embed.add_field(name="**<:icon_owner:947357468101582849> __Owner__**", value=f'''
[AE・ARTHISHᵍᶠˣ](https://discord.com/users/315342835283001344)
''')
        embed.add_field(name="**<:icon_ping:947358103941300295> __Ping__**", value=f'''
{round(self.client.latency*1000)}ms
''')

        embed.add_field(name="**<:changelog:947139030800269373> __Language__**", value=f'''
Discord.py 2.0
''')
        uptime = uptime = str(datetime.timedelta(
            seconds=int(round(time.time()-startTime))))
        embed.add_field(name="<:icon_clock:947357599030997043> **__Uptime__**", value=f'''
{uptime}
''')

        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")

        await ctx.send(embed=embed)

    @commands.command(name='source', pass_context=True, case_insensitive=True, aliases=['src'], help="Hehe")
    async def source(self, ctx):
        await ctx.send("https://c.tenor.com/UK49dL7MKmkAAAAC/dil-se-bura-lagta-hai-bhai-please-bhai-looks-heartbreaking.gif")


async def setup(client):
    await client.add_cog(Misc(client))
