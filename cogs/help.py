import discord
from discord.ext import commands


class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(name="help", pass_context=True, invoke_without_command=True, case_insensitive=True, aliases=['h', 'Help', 'HELP'])
    async def help(self, ctx):

        embed = discord.Embed(title="Axom | Command List",
                              description="<:line_top:947143646334042122> My Prefix Is `&`\n<:line_bottom:947143905810473050> I Am A Bot For Calculating Games Points & Making Leaderboards.", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:leaderb:947178467156430868> Leaderboard Commands", value='''
**```
tourneychannels,tourneydelete,
tourneyunhide,tourneyhide,
tourneyinfo
```**
''')
        embed.add_field(name="<:awardicon:954265063907283005> Tourney Helper Commands", value='''
**```
leaderboard,newcalculate,
ptsetup,slotlist
```**
''')
        embed.add_field(name='<:box:947178898553204736> Misc Commands', value='''
**```
ping,preview,source 
```**
''')
        embed.add_field(name='<:icon_link:947337569299996712> Useful Links', value='''
**<:support:947181084863520858> | [Support Server](https://discord.gg/uW7WXxBtBW)
<:bot:947181167990423562> | [Invite The Bot](https://discord.com/api/oauth2/authorize?client_id=908949899645706241&permissions=2952916049&scope=bot%20applications.commands)
<:like:947180731656994866> | [Vote Me](https://top.gg/bot/880314360017338380/vote)
**
''')
        await ctx.send(embed=embed)

    @help.command(name='leaderboard', pass_context=True, case_insensitive=True, aliases=['lb'])
    async def leaderboard(self, ctx):
        embed = discord.Embed(
            title="Leaderboard", description="This Command Help You To Make Cool-Looking Leaderboards, Current We Only Have 2 Free Designs", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage", value='''
**```
&leaderboard
```**
''')
        embed.add_field(name="<:icon_alias:947347903511404555> Aliases", value='''
**```
leaderb,lb
```**
''')
        await ctx.send(embed=embed)

    @help.command(name='preview', pass_context=True, case_insensitive=True, aliases=['pv', 'prev'])
    async def preview(self, ctx):
        embed = discord.Embed(
            title="Preview", description="Look At The Available Free Designs Using This Command ", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage", value='''
**```
&preview
```**
''')
        embed.add_field(name="<:icon_alias:947347903511404555> Aliases", value='''
**```
prev,pv
```**
''')
        await ctx.send(embed=embed)

    @help.command(name='ncalculate', pass_context=True, case_insensitive=True, aliases=['ncalc'])
    async def newcalculate(self, ctx):
        embed = discord.Embed(title="Ncalculate", description="Calculate Points Of Matches & Give In Format Such That Can Be Used In Leaderboard Command\n<:iconwarning:946654059715244033> | Currently We Only Support BGMI Points System", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage", value='''
**```
&ncalculate
```**
''')
        embed.add_field(name="<:icon_alias:947347903511404555> Aliases", value='''
**```
ncalc
```**
''')
        await ctx.send(embed=embed)

    @help.command(name='ptsetup', pass_context=True, case_insensitive=True, aliases=['pts'])
    async def ptsetup(self, ctx):
        embed = discord.Embed(
            title="Ptsetup", description="Makes A `PT-Mod` Role, People With This Role Can Use The Leaderboard Commands Even If They Dont Have The `Manage Messages` Permission", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage", value='''
**```
&ptsetup
```**
''')
        embed.add_field(name="<:icon_alias:947347903511404555> Aliases", value='''
**```
pts
```**
''')
        await ctx.send(embed=embed)

    @help.command(name='slotlist', pass_context=True, case_insensitive=True, aliases=['sl', 'slot'])
    async def slotlist(self, ctx):
        embed = discord.Embed(title="Slotlist", description="This Will Give You The 2 Formats To Fill Which You Will Be Using While Points Calculation: \n<:px_no1:938969002401730561> | Team Prefixes Format, To Fill With The Team Prefixes\n<:px_no2:938969171742588988> | Match Points Format, To Fill With Match Points Using The Prefixes Given In Team Prefixes Format", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage", value='''
**```
&slotlist
```**
''')
        embed.add_field(name="<:icon_alias:947347903511404555> Aliases", value='''
**```
sl,slot
```**
''')
        await ctx.send(embed=embed)

    @help.command(name='tourneychannels', pass_context=True, case_insensitive=True, aliases=["tchannels", "tc"])
    async def tourneychannels(self, ctx):
        embed = discord.Embed(
            title="Tourney Channels", description="This Will Allow You To Quickly Create Tournament Channels", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage", value='''
**```
&tourneychannels
```**
''')
        embed.add_field(name="<:icon_alias:947347903511404555> Aliases", value='''
**```
tchannels,tc
```**
''')
        await ctx.send(embed=embed)

    @help.command(name='tourneydelete', pass_context=True, case_insensitive=True, aliases=["tdelete", "td"])
    async def tourneydelete(self, ctx):
        embed = discord.Embed(
            title="Tourney Delete", description="This Will Allow You To DELETE Any Category With All Its Channels", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage", value='''
**```
&tourneydelete
```**
''')
        embed.add_field(name="<:icon_alias:947347903511404555> Aliases", value='''
**```
tdelete,td
```**
''')
        await ctx.send(embed=embed)

    @help.command(name='tourneyunhide', pass_context=True, case_insensitive=True, aliases=["tunhide", "tuh"])
    async def tourneyunhide(self, ctx):
        embed = discord.Embed(
            title="Tourney Unhide", description="This Will Allow You To UNHIDE Any Category With All Its Channels", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage", value='''
**```
&tourneyunhide
```**
''')
        embed.add_field(name="<:icon_alias:947347903511404555> Aliases", value='''
**```
tunhide,tuh
```**
''')
        await ctx.send(embed=embed)

    @help.command(name='tourneyhide', pass_context=True, case_insensitive=True, aliases=["thide", "th"])
    async def tourneyhide(self, ctx):
        embed = discord.Embed(
            title="Tourney Hide", description="This Will Allow You To HIDE Any Category With All Its Channels", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage", value='''
**```
&tourneyhide
```**
''')
        embed.add_field(name="<:icon_alias:947347903511404555> Aliases", value='''
**```
thide,th
```**
''')
        await ctx.send(embed=embed)

    @help.command(name='tourneyinfo', pass_context=True, case_insensitive=True, aliases=["tinfo", "ti"])
    async def tourneyinfo(self, ctx):
        embed = discord.Embed(
            title="Tourney Info", description="This Will Allow You To Send Info Of Your Tournament To A Channel", color=discord.Colour.gold())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.client.user.display_avatar.url)
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage", value='''
**```
&tourneyinfo
```**
''')
        embed.add_field(name="<:icon_alias:947347903511404555> Aliases", value='''
**```
tinfo,ti
```**
''')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(help(client))
