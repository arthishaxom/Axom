import discord
from discord.ext import commands



class help(commands.Cog):

	def __init__(self, client):
			self.client = client

	@commands.group(name="help",pass_context = True,invoke_without_command = True,case_insensitive = True,aliases = ['h','Help','HELP'])
	async def help(self, ctx):
			
			embed = discord.Embed(title = "Axom | Command List",description = "<:line_top:947143646334042122> My Prefix Is `&`\n<:line_bottom:947143905810473050> I Am A Bot For Calculating Games Points & Making Leaderboards.",color = discord.Colour.gold())
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
			embed.set_thumbnail(url=self.client.user.display_avatar.url)
			embed.set_footer(text = "Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
			embed.add_field(name="<:leaderb:947178467156430868> Leaderboard Commands",value = '''
**```
leaderboard,newcalculate,
ptsetup,slotlist
```**
''')
			embed.add_field(name='<:box:947178898553204736> Misc Commands',value = '''
**```
ping,preview   
```**
''')
			embed.add_field(name='<:icon_link:947337569299996712> Useful Links',value = '''
**<:support:947181084863520858> | [Support Server](https://discord.gg/uW7WXxBtBW)
<:bot:947181167990423562> | [Invite The Bot](https://discord.com/oauth2/authorize?client_id=880314360017338380&permissions=268561601&scope=bot)
<:bot:947181167990423562> | [Vote Me](https://top.gg/bot/880314360017338380/vote)
**
''')
			await ctx.send(embed=embed)

	@help.command(name ='leaderboard',pass_context = True,case_insensitive = True,aliases = ['lb'])
	async def leaderboard(self,ctx):
			embed = discord.Embed(title = "Leaderboard",description = "This Command Help You To Make Cool-Looking Leaderboards, Current We Only Have 2 Free Designs",color = discord.Colour.gold())
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
			embed.set_thumbnail(url=self.client.user.display_avatar.url)
			embed.set_footer(text = "Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
			embed.add_field(name="<:icon_supp:938970921702678548> Usage",value = '''
**```
&leaderboard
```**
''')
			embed.add_field(name="<:icon_supp:938970921702678548> Aliases",value = '''
**```
leaderb,lb
```**
''')
			await ctx.send(embed=embed)

	@help.command(name ='preview',pass_context = True,case_insensitive = True,aliases = ['pv','prev'])
	async def preview(self,ctx):
			embed = discord.Embed(title = "Preview",description = "Look At The Available Free Designs Using This Command ",color = discord.Colour.gold())
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
			embed.set_thumbnail(url=self.client.user.display_avatar.url)
			embed.set_footer(text = "Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
			embed.add_field(name="<:icon_supp:938970921702678548> Usage",value = '''
**```
&preview
```**
''')
			embed.add_field(name="<:icon_supp:938970921702678548> Aliases",value = '''
**```
prev,pv
```**
''')
			await ctx.send(embed=embed)

	@help.command(name ='newcalculate',pass_context = True,case_insensitive = True,aliases = ['ncalc'])
	async def newcalculate(self,ctx):
			embed = discord.Embed(title = "Newcalculate",description = "Calculate Points Of Matches & Give In Format Such That Can Be Used In Leaderboard Command\n<a:excla_blue:939127974878380042> | Currently We Only Support BGMI Points System",color = discord.Colour.gold())
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
			embed.set_thumbnail(url=self.client.user.display_avatar.url)
			embed.set_footer(text = "Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
			embed.add_field(name="<:icon_supp:938970921702678548> Usage",value = '''
**```
&newcalculate
```**
''')
			embed.add_field(name="<:icon_supp:938970921702678548> Aliases",value = '''
**```
ncalc
```**
''')
			await ctx.send(embed=embed)

	@help.command(name ='ptsetup',pass_context = True,case_insensitive = True,aliases = ['pts'])
	async def ptsetup(self,ctx):
			embed = discord.Embed(title = "Ptsetup",description = "Makes A `PT-Mod` Role, People With This Role Can Use The Leaderboard Commands Even If They Dont Have The `Manage Messages` Permission",color = discord.Colour.gold())
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
			embed.set_thumbnail(url=self.client.user.display_avatar.url)
			embed.set_footer(text = "Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
			embed.add_field(name="<:icon_supp:938970921702678548> Usage",value = '''
**```
&ptsetup
```**
''')
			embed.add_field(name="<:icon_supp:938970921702678548> Aliases",value = '''
**```
pts
```**
''')
			await ctx.send(embed=embed)

	@help.command(name ='slotlist',pass_context = True,case_insensitive = True,aliases = ['sl','slot'])
	async def slotlist(self,ctx):
			embed = discord.Embed(title = "Ptsetup",description = "This Will Give You The 2 Formats To Fill Which You Will Be Using While Points Calculation: \n<:px_no1:938969002401730561> | Team Prefixes Format, To Fill With The Team Prefixes\n<:px_no2:938969171742588988> | Match Points Format, To Fill With Match Points Using The Prefixes Given In Team Prefixes Format",color = discord.Colour.gold())
			embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
			embed.set_thumbnail(url=self.client.user.display_avatar.url)
			embed.set_footer(text = "Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
			embed.add_field(name="<:icon_supp:938970921702678548> Usage",value = '''
**```
&slotlist
```**
''')
			embed.add_field(name="<:icon_supp:938970921702678548> Aliases",value = '''
**```
sl,slot
```**
''')
			await ctx.send(embed=embed)



def setup(client):
    client.add_cog(help(client)) 