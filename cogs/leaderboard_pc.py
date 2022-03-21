import discord
import os
import asyncio
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from discord.ext.commands.core import bot_has_permissions
from discord.utils import get
from Functions.helpful_lb import top20, top25


class Leaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='ptsetup', aliases=['pts'], case_insensitive=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(manage_guild=True, manage_roles=True)
    async def _ptsetup(self, ctx):
        guilded = ctx.guild
        if get(ctx.guild.roles, name="PT-Mod"):
            await ctx.send("Role Is Already Created")
            return
        else:
            await guilded.create_role(name="PT-Mod", color=discord.Colour.gold())
            await ctx.send("Created Role!, Now People With This Role Can Use My Commands Even If They Don' Have Manage_Messages Perms.")

    @commands.command(name='preview', aliases=['prev', 'pv'], case_insensitive=True)
    @commands.bot_has_permissions(manage_messages=True, embed_links=True, attach_files=True)
    @bot_has_permissions(attach_files=True)
    async def _preview(self, ctx):
        pic = discord.Embed(title="__BOARD 1__", color=discord.Colour.gold())
        file = discord.File(r'./PREVS/BOARD-1.png')
        pic.set_image(url='attachment://BOARD-1.png')
        pic2 = discord.Embed(title="__BOARD 2__", color=discord.Colour.gold())
        file2 = discord.File(r'./PREVS/BOARD-2.png')
        pic2.set_image(url='attachment://BOARD-2.png')
        await ctx.send(file=file, embed=pic)
        await ctx.send(file=file2, embed=pic2)

    @commands.command(name="slotlist", aliases=['sl', 'slot'], case_insensitive=True)
    @commands.bot_has_permissions(manage_messages=True, embed_links=True, attach_files=True)
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.has_role('PT-Mod'), commands.is_owner())
    async def slotlist(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        try:
            msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except:
            await ctx.send("**`Send Slotlist`**")
            try:
                msg = await self.client.wait_for("message", timeout=120, check=check)
                slotlist = msg.content
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=discord.Colour.red())
                await ctx.send(embed=embed)
                return
        try:
            listslot = slotlist.splitlines()
        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=discord.Colour.red())
            await ctx.send(embed=embed)
            return
        await ctx.send('''**`Type Delimiter : 
For Example : 3) TEAM XYZ
Here, ) Is The Delimeter`**''')
        try:
            input2 = await self.client.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=discord.Colour.red())
            await ctx.send(embed=embed)
            return
        delimeter = input2.content
        try:
            listslot2 = []
            for i in range(len(listslot)):
                e = listslot[i].split(f'{delimeter}')
                listslot2.append(e[0]+",,"+e[1].strip())
            slotsmsg = "\n".join(listslot2)
            await ctx.send(f"**`{slotsmsg}`**")
            nlist = ["1,,", "2,,", "3,,", "4,,", "5,,", "6,,", "7,,", "8,,", "9,,", "10,,", "11,,", "12,,", "13,,",
                     "14,,", "15,,", "16,,", "17,,", "18,,", "19,,", "20,,", "21,,", "22,,", "23,,", "24,,", "25,,"]
            await ctx.send("\n".join(nlist[:len(listslot)]))
        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=discord.Colour.red())
            await ctx.send(embed=embed)
            return

    @commands.command(name="leaderboard", aliases=['leaderb', 'lb'], case_insensitive=True)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.bot_has_permissions(manage_messages=True, embed_links=True, attach_files=True)
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.has_role('PT-Mod'), commands.is_owner())
    async def _leaderboard(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        try:
            embed1 = discord.Embed(title='**__SEND FORMAT__**', description='''
**```
TEAM1,TEAM2,...
CHICKEN1,CHICKEN2,...
POSITON1,POSTION2,...
KILL1,KILL2,...
TOTAL1,TOTAL2,...
```**
''', color=discord.Colour.gold())
            embed1.set_footer(text='Besure To Have Atleast 2 Teams')
            embed_msg = await ctx.send(embed=embed1)
            try:
                msg = await self.client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=discord.Colour.red())
                await ctx.send(embed=embed)
                return

            data = msg.content
            datas = data.splitlines()
        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=discord.Colour.red())
            await ctx.send(embed=embed)
            return

        try:
            splitedte = datas[0].split(",")

            splitedcd = datas[1].split(",")

            splitedpos = datas[2].split(",")

            splitedkill = datas[3].split(",")

            splitedtotal = datas[4].split(",")

        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=discord.Colour.red())
            await ctx.send(embed=embed)
            return

        pguilds = [667103945503670282]
        if ctx.message.guild.id not in pguilds:
            embed2 = discord.Embed(title='**ENTER TITLE & SUBTITLE**', description='''
> Title,Subitle
> Example : T3 SCRIMS,XYZ ESPORTS
<a:red:938971541662761001> Length Of The Titles Should Under 15.
''', color=discord.Colour.gold())
            embed2.set_footer(text='Spaces Are Also Counted.')
            await msg.delete()
            await embed_msg.edit(embed=embed2)
            try:
                msg = await self.client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=discord.Colour.red())
                await ctx.send(embed=embed)
                return
            try:
                title = msg.content
                title = title.split(",")
            except Exception as e:
                embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                      description=f'The Error : \n{e}', color=discord.Colour.red())
                await ctx.send(embed=embed)
                return

        if ctx.message.guild.id in pguilds:
            embed3 = discord.Embed(title='**__CHOOSE AN OPTION__**', description='''
**` 1 ` T2 SCRIMS [ACOLYTE]
` 2 ` T2Q SCRIMS [ACOLYTE]
` 3 ` VETERAN SCRIMS [ACOLYTE]
` 4 ` T2Q SCRIMS [ACOLYTE]**
''', color=discord.Colour.gold())
            await embed_msg.edit(embed=embed3)
        else:
            embed3 = discord.Embed(title='**__CHOOSE AN OPTION__**', description='''
**` 1 ` BOARD 1
` 2 ` BOARD 2**
''', color=discord.Colour.gold())
            await embed_msg.edit(embed=embed3)

        if ctx.message.guild.id in pguilds:
            file_paths = {1: r'./RAWS/T2_AE.png', 2: r'./RAWS/T2Q_AE.png',
                          3: r'./RAWS/VETERAN_AE.png', 4: r'./RAWS/AE-T1Q.png'}
        else:
            if len(splitedte) > 20:
                file_paths = {1: r'./RAWS/BOARD-1_25.png',
                              2: r'./RAWS/BOARD-2_25.png'}
            else:
                file_paths = {1: r'./RAWS/BOARD-1.png',
                              2: r'./RAWS/BOARD-2.png'}

        colors = {1: r'#25e4d4', 2: r'#ff5500'}

        server_nname = ctx.message.guild.name
        server_name = ''
        for i in server_nname:
            if i.isalnum():
                server_name += i
        try:
            await msg.delete()
            msg = await self.client.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=discord.Colour.red())
            await ctx.send(embed=embed)
            return
        reply = msg.content
        try:
            lb = Image.open(f'{file_paths[int(reply)]}').convert('RGBA')
        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=discord.Colour.red())
            await ctx.send(embed=embed)
            return

        try:
            copy = lb.copy()
            copy.save(rf"./COPIES/{server_name}here.png")
            here = Image.open(rf"./COPIES/{server_name}here.png")
        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=discord.Colour.red())
            await ctx.send(embed=embed)
            return
        #Files & Fonts
        draw = ImageDraw.Draw(here)
        fontsFolder = rf'./FONTS'
        TitleFont1 = ImageFont.truetype(
            os.path.join(fontsFolder, 'Moonrising.ttf'), 139)
        TitleFont2 = ImageFont.truetype(
            os.path.join(fontsFolder, 'Moonrising.ttf'), 67)
        TextFont1 = ImageFont.truetype(
            os.path.join(fontsFolder, 'Retroica.ttf'), 25)
        global times_used

        await msg.delete()
        embed4 = discord.Embed(
            description="**Please Wait <a:icon_loading:939409269978177546>**", color=discord.Colour.gold())
        await embed_msg.edit(embed=embed4)

        if ctx.message.guild.id not in pguilds:
            try:
                if len(splitedte) > 20:
                    top25.title(draw, title, TitleFont1,
                                TitleFont2, colors, reply)
                else:
                    top20.title(draw, title, TitleFont1,
                                TitleFont2, colors, reply)
            except Exception as e:
                embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                      description=f'The Error : \n{e}', color=discord.Colour.red())
                await ctx.send(embed=embed)
                os.remove(rf'./COPIES/{server_name}here.png')
                return

        try:
            if len(splitedte) > 25:
                splitedte = splitedte[:26]
                splitedcd = splitedcd[:26]
                splitedpos = splitedpos[:26]
                splitedkill = splitedkill[:26]
                splitedtotal = splitedtotal[:26]
            if len(splitedte) > 20:
                top25.splitedte(draw, splitedte, TextFont1)
                top25.splitedcd(draw, splitedcd, TextFont1)
                top25.splitedpos(draw, splitedpos, TextFont1)
                top25.splitedkill(draw, splitedkill, TextFont1)
                top25.splitedtotal(draw, splitedtotal, TextFont1)
            else:
                top20.splitedte(draw, splitedte, TextFont1)
                top20.splitedcd(draw, splitedcd, TextFont1)
                top20.splitedpos(draw, splitedpos, TextFont1)
                top20.splitedkill(draw, splitedkill, TextFont1)
                top20.splitedtotal(draw, splitedtotal, TextFont1)

            here.save(rf'./RESULTS/{server_name}BOARD1-RESULT.png')
            file = discord.File(rf'./RESULTS/{server_name}BOARD1-RESULT.png')
            embed5 = discord.Embed(
                title="**Done <a:icon_done:939411770458640425>**", color=discord.Colour.gold())
            embed5.set_image(
                url=rf"attachment://{server_name}BOARD1-RESULT.png")
            await ctx.send(embed=embed5, file=file)
            await embed_msg.delete()
            os.remove(rf'./RESULTS/{server_name}BOARD1-RESULT.png')
            os.remove(rf"./COPIES/{server_name}here.png")

        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=discord.Colour.red())
            embed.set_footer(text='Besure To Have Atleast 2')
            await ctx.send(embed=embed)
            os.remove(rf'./RESULTS/{server_name}BOARD1-RESULT.png')
            os.remove(rf"./COPIES/{server_name}here.png")


async def setup(client):
    await client.add_cog(Leaderboard(client))
