import discord
import os
import asyncio
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from discord.utils import get
from Utilities.helpful_lb import top20, top25, top10, top12
import functools
import io
from Utilities.BotColoursInfo import BotColours
from discord.ui import Button, View
import traceback
from Utilities.cooldownfunc import bypass_for_owner2
import ntpath
import traceback


class Feedback(discord.ui.Modal, title='LeaderBoard Input'):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    maintitle = discord.ui.TextInput(
        label='Title',
        placeholder='Example - T3 SCRIMS',
        required=True
    )
    subtitle = discord.ui.TextInput(
        label='Subtitle',
        placeholder='Example - XYZ ESPORTS',
        required=True
    )

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    maindata = discord.ui.TextInput(
        label='Points',
        style=discord.TextStyle.long,
        placeholder='''TEAM1,TEAM2,...
CHICKEN1,CHICKEN2,...
POSITON1,POSTION2,...
KILL1,KILL2,...
TOTAL1,TOTAL2,...''',
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        self.interaction = interaction
        await self.interaction.response.defer()
        self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)


class MyView(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None
        self.response = None

    @discord.ui.button(label="Continue", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction, button):
        feedback_modal = Feedback()
        await interaction.response.send_modal(feedback_modal)
        # await interaction.response.send_message(view=self)
        try:
            await feedback_modal.wait()
            self.value = [feedback_modal.maintitle.value,
                          feedback_modal.subtitle.value, feedback_modal.maindata.value]
            self.stop()
        except:
            pass

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def no_button_callback(self, interaction, button):
        for item in self.children:
            item.disabled = True
        await interaction.response.defer()
        await interaction.message.edit(view=self)
        self.value = "no"
        self.stop()

    @discord.ui.button(emoji="<:Icon_Ques:970222585088466984>", style=discord.ButtonStyle.grey)
    async def help_callback(self, interaction, button):
        await interaction.response.send_message('''
For Getting Points In This Format, You Can Use The `&calculate2` Command, Which Gives You The Points In The Format, You Just Have To Copy It.
> **If You Already Have The Points __Calculated & Sorted__ Then Just Write Them In The Format Mentioned And Keep It Copied**
If You Have Any Other Issue, You Can Join The Support Server: 
https://discord.gg/uW7WXxBtBW
''', ephemeral=True)
        # self.value = "help"
        # self.stop()

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.response.edit(content="**Timeouted**", view=self)
        return

    async def interaction_check(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            return await interaction.response.send_message(content=f"You can't do that! Only {self.ctx.author.mention} can do that!", ephemeral=True)
        return True


class BoardButtons(Button):
    def __init__(self, label):
        super().__init__(label=f"{label}",
                         style=discord.ButtonStyle.grey)

    async def callback(self, interaction):
        self.view.value = self.label
        self.view.clear_items()
        await interaction.response.edit_message(view=self.view)
        self.view.stop()


class MySelectView(View):
    def __init__(self, ctx, dicti, length):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None
        for i in dicti.keys():
            pathoffile = dicti[i]
            name = ntpath.basename(pathoffile)[:-4]
            self.add_item(BoardButtons(name))
        self.length = length

    @discord.ui.button(label="Preview", style=discord.ButtonStyle.blurple)
    async def preview_callback(self, interaction, button):
        if self.length > 10:
            pic = discord.Embed(title="BOARD 1", color=BotColours.main())
            file = discord.File(r'./PREVS/20 STYLES/BOARD-1.png')
            pic.set_image(url=r'attachment://BOARD-1.png')
            pic2 = discord.Embed(title="BOARD 2", color=BotColours.main())
            file2 = discord.File(r'./PREVS/20 STYLES/BOARD-2.png')
            pic2.set_image(url=r'attachment://BOARD-2.png')
            pic3 = discord.Embed(title="BOARD 3", color=BotColours.main())
            file3 = discord.File(r'./PREVS/20 STYLES/BOARD-3.png')
            pic3.set_image(url=r'attachment://BOARD-3.png')
            pic4 = discord.Embed(title="BOARD 4", color=BotColours.main())
            file4 = discord.File(r'./PREVS/20 STYLES/BOARD-4.png')
            pic4.set_image(url=r'attachment://BOARD-4.png')
            button.disabled = True
            await interaction.response.edit_message(view=self)
            # await interaction.response.defer()
            await interaction.followup.send(embeds=[pic, pic2, pic3, pic4], files=[file, file2, file3, file4], ephemeral=True)

        else:
            pic = discord.Embed(title="BOARD 1", color=BotColours.main())
            file = discord.File(r'./PREVS/10 STYLES/BOARD-1.png')
            pic.set_image(url=r'attachment://BOARD-1.png')
            pic2 = discord.Embed(title="BOARD 2", color=BotColours.main())
            file2 = discord.File(r'./PREVS/10 STYLES/BOARD-2.png')
            pic2.set_image(url=r'attachment://BOARD-2.png')
            pic3 = discord.Embed(title="BOARD 3", color=BotColours.main())
            file3 = discord.File(r'./PREVS/10 STYLES/BOARD-3.png')
            pic3.set_image(url=r'attachment://BOARD-3.png')
            pic4 = discord.Embed(title="BOARD 4", color=BotColours.main())
            file4 = discord.File(r'./PREVS/10 STYLES/BOARD-4.png')
            pic4.set_image(url=r'attachment://BOARD-4.png')
            button.disabled = True
            await interaction.response.edit_message(view=self)
            # await interaction.response.defer()
            await interaction.followup.send(files=[file, file2, file3, file4], embeds=[pic, pic2, pic3, pic4], ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            return await interaction.response.send_message(content=f"You can't do that! Only {self.ctx.author.mention} can do that!", ephemeral=True)
        return True

    async def on_timeout(self):
        return


class MyPreview(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.response = None

    @discord.ui.button(label="Top 10", style=discord.ButtonStyle.grey)
    async def top10_callback(self, interaction, button):
        pic = discord.Embed(title="BOARD 1", color=BotColours.main())
        file = discord.File(r'./PREVS/10 STYLES/BOARD-1.png')
        pic.set_image(url=r'attachment://BOARD-1.png')
        pic2 = discord.Embed(title="BOARD 2", color=BotColours.main())
        file2 = discord.File(r'./PREVS/10 STYLES/BOARD-2.png')
        pic2.set_image(url=r'attachment://BOARD-2.png')
        pic3 = discord.Embed(title="BOARD 3", color=BotColours.main())
        file3 = discord.File(r'./PREVS/10 STYLES/BOARD-3.png')
        pic3.set_image(url=r'attachment://BOARD-3.png')
        pic4 = discord.Embed(title="BOARD 4", color=BotColours.main())
        file4 = discord.File(r'./PREVS/10 STYLES/BOARD-4.png')
        pic4.set_image(url=r'attachment://BOARD-4.png')
        button.disabled = True
        await interaction.response.edit_message(view=self)
        # await interaction.response.defer()
        await interaction.followup.send(files=[file, file2, file3, file4], embeds=[pic, pic2, pic3, pic4])

    @discord.ui.button(label="Top 20", style=discord.ButtonStyle.grey)
    async def top20_callback(self, interaction, button):
        pic = discord.Embed(title="BOARD 1", color=BotColours.main())
        file = discord.File(r'./PREVS/20 STYLES/BOARD-1.png')
        pic.set_image(url=r'attachment://BOARD-1.png')
        pic2 = discord.Embed(title="BOARD 2", color=BotColours.main())
        file2 = discord.File(r'./PREVS/20 STYLES/BOARD-2.png')
        pic2.set_image(url=r'attachment://BOARD-2.png')
        pic3 = discord.Embed(title="BOARD 3", color=BotColours.main())
        file3 = discord.File(r'./PREVS/20 STYLES/BOARD-3.png')
        pic3.set_image(url=r'attachment://BOARD-3.png')
        pic4 = discord.Embed(title="BOARD 4", color=BotColours.main())
        file4 = discord.File(r'./PREVS/20 STYLES/BOARD-4.png')
        pic4.set_image(url=r'attachment://BOARD-4.png')
        button.disabled = True
        await interaction.response.edit_message(view=self)
        # await interaction.response.defer()
        await interaction.followup.send(embeds=[pic, pic2, pic3, pic4], files=[file, file2, file3, file4])

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.response.edit(view=self)
        return

    async def interaction_check(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            return await interaction.response.send_message(content=f"You can't do that! Only {self.ctx.author.mention} can do that!", ephemeral=True)
        return True


class Leaderboard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='ptsetup', aliases=['pts'], case_insensitive=True, help="Makes A Role `PT-Mod`, People With This Role Can Use Leaderboard Command Even If They Don't Have Manage_Messages Perms.")
    @commands.bot_has_permissions(manage_roles=True)
    @commands.check_any(commands.has_permissions(manage_roles=True), commands.has_role('PT-Mod'), commands.is_owner())
    async def _ptsetup(self, ctx):
        guilded = ctx.guild
        if get(ctx.guild.roles, name="PT-Mod"):
            await ctx.send("Role Is Already Created")
            return
        else:
            await guilded.create_role(name="PT-Mod", color=BotColours.main())
            await ctx.send("Created Role!, Now People With This Role Can Use My Commands Even If They Don't Have Manage_Messages Perms.")

    @commands.command(name='preview', aliases=['prev', 'pv'], case_insensitive=True, help="Shows The Leaderboards Preview")
    @commands.bot_has_permissions(embed_links=True, attach_files=True)
    async def _preview(self, ctx):
        view = MyPreview(ctx)
        embed_msg = await ctx.send(embed=discord.Embed(title="Choose Which Boards You Want To See.", color=BotColours.main()), view=view)
        view.response = embed_msg
        res = await view.wait()
        if res:
            return

    @commands.command(name="leaderboard", aliases=['leaderb', 'lb'], case_insensitive=True, help='''Makes The Leaderboards As Per This Format:
**```
TEAM1,TEAM2,...
CHICKEN1,CHICKEN2,...
POSITON1,POSTION2,...
KILL1,KILL2,...
TOTAL1,TOTAL2,...
```**

Use `&c1` Or `&c2` To Get The Points In This Format.''')
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    @commands.bot_has_permissions(manage_messages=True, embed_links=True, attach_files=True)
    @commands.dynamic_cooldown(bypass_for_owner2, commands.BucketType.guild)
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.has_role('PT-Mod'), commands.is_owner())
    async def _leaderboard(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        def openingFile(file_paths, reply, server_name):
            lb = Image.open(f'{file_paths[reply]}').convert('RGBA')

            # copy =
            # copy.save(rf"./COPIES/{server_name}here.png")
            # here = Image.open(rf"./COPIES/{server_name}here.png")
            here = lb.copy()
            draw = ImageDraw.Draw(here)
            return draw, here

        def making_board(here, draw, TextFont1, splitedte, splitedcd, splitedpos, splitedkill, splitedtotal, custominput):

            if custominput != "no":
                if len(splitedte) > 20:
                    top25.title(draw, title, TitleFont1,
                                TitleFont2, colors, reply)
                elif len(splitedte) <= 10:
                    top10.title(draw, title, TitleFont3,
                                TitleFont4, colors, reply)
                elif len(splitedte) > 10 and len(splitedte) <= 12:
                    top12.title(draw, title, TitleFont3,
                                TitleFont4, colors, reply)
                else:
                    top20.title(draw, title, TitleFont1,
                                TitleFont2, colors, reply)
            if len(splitedte) > 20:
                top25.splitedte(draw, splitedte, TextFont1)
                top25.splitedcd(draw, splitedcd, TextFont1)
                top25.splitedpos(draw, splitedpos, TextFont1)
                top25.splitedkill(draw, splitedkill, TextFont1)
                top25.splitedtotal(draw, splitedtotal, TextFont1)
            elif len(splitedte) <= 10:
                top10.splitedte(draw, splitedte, TextFont1)
                top10.splitedcd(draw, splitedcd, TextFont1)
                top10.splitedpos(draw, splitedpos, TextFont1)
                top10.splitedkill(draw, splitedkill, TextFont1)
                top10.splitedtotal(draw, splitedtotal, TextFont1)
            elif len(splitedte) > 10 and len(splitedte) <= 12:
                top12.splitedte(draw, splitedte, TextFont1)
                top12.splitedcd(draw, splitedcd, TextFont1)
                top12.splitedpos(draw, splitedpos, TextFont1)
                top12.splitedkill(draw, splitedkill, TextFont1)
                top12.splitedtotal(draw, splitedtotal, TextFont1)
            else:
                top20.splitedte(draw, splitedte, TextFont1)
                top20.splitedcd(draw, splitedcd, TextFont1)
                top20.splitedpos(draw, splitedpos, TextFont1)
                top20.splitedkill(draw, splitedkill, TextFont1)
                top20.splitedtotal(draw, splitedtotal, TextFont1)
            with io.BytesIO() as a:
                here.save(a, "png")
                a.seek(0)
                file = discord.File(
                    a, filename=rf"{server_name}BOARD1-RESULT.png")
            return file
        view = MyView(ctx)
        embed1 = discord.Embed(title='**GETTING STARTED**', description='''
For Making Leaderboards, You Would Need The Points In The Following Format:
**```
TEAM1,TEAM2,...
CHICKEN1,CHICKEN2,...
POSITON1,POSTION2,...
KILL1,KILL2,...
TOTAL1,TOTAL2,...
```**
> **If You Don't Know How To Make This Format Click On The "<:Icon_Ques:970222585088466984>" Button.**
''', color=BotColours.main())
        embed1.set_footer(text='Be Sure To Have Atleast 2 Teams')
        embed_msg = await ctx.send(embed=embed1, view=view)
        view.response = embed_msg
        # try:
        #     msg = await self.client.wait_for("message", timeout=30, check=check)
        # except asyncio.TimeoutError:
        #     msg.delete()
        #     embed = discord.Embed(
        #         title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=BotColours.error())
        #     await ctx.send(embed=embed)
        #     return
        res = await view.wait()
        if res:
            return
        if view.value == "no":
            return
        Modal_DataList = view.value
        title = [Modal_DataList[0], Modal_DataList[1]]
        data = Modal_DataList[2]
        datas = data.splitlines()
        # except Exception as e:
        #     embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
        #                           description=f'The Error : \n{e}', color=BotColours.error())
        #     await ctx.send(embed=embed)
        #     return
        if len(datas) < 5:
            view.clear_items()
            await embed_msg.edit(view=view)
            await ctx.send(f'**<:iconwarning:946654059715244033> Please Send Correct Points Format.**')
            return
        try:
            splitedte = datas[0].split(",")

            splitedcd = datas[1].split(",")

            splitedpos = datas[2].split(",")

            splitedkill = datas[3].split(",")

            splitedtotal = datas[4].split(",")

        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=BotColours.error())
            await ctx.send(embed=embed)
            return

        pguilds = []
        file_paths = {}
        colors = {}
        limit = 25
        Titlecolor = "no"
        custominput = "default"
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                data = await connection.fetch(f'''SELECT * FROM premium WHERE serverid = $1''', ctx.message.guild.id)
                # ./RAWS/BLACKLIGHT/3 PM.png;;./RAWS/BLACKLIGHT/4 PM.png"
        if data != []:
            filepaths = (data[0][1]).split(";;")
            for filepath in filepaths:
                file_paths[ntpath.basename(filepath)[:-4]] = rf"{filepath}"
            limit = data[0][2]
            custominput = data[0][3]
            Titlecolor = data[0][4]

        else:
            if len(splitedte) > 20:
                file_paths = {"BOARD 1": r'./RAWS/25 STYLES/BOARD 1.png',
                              "BOARD 2": r'./RAWS/25 STYLES/BOARD 2.png',
                              "BOARD 3": r'./RAWS/25 STYLES/BOARD 3.png',
                              "BOARD 4": r'./RAWS/25 STYLES/BOARD 4.png', }
            elif len(splitedte) <= 10:
                file_paths = {"BOARD 1": r'./RAWS/10 STYLES/BOARD 1.png',
                              "BOARD 2": r'./RAWS/10 STYLES/BOARD 2.png',
                              "BOARD 3": r'./RAWS/10 STYLES/BOARD 3.png',
                              "BOARD 4": r'./RAWS/10 STYLES/BOARD 4.png', }
            elif len(splitedte) > 10 and len(splitedte) <= 12:
                file_paths = {"BOARD 1": r'./RAWS/12 STYLES/BOARD 1.png',
                              "BOARD 2": r'./RAWS/12 STYLES/BOARD 2.png',
                              "BOARD 3": r'./RAWS/12 STYLES/BOARD 3.png',
                              "BOARD 4": r'./RAWS/12 STYLES/BOARD 4.png', }
            else:
                file_paths = {"BOARD 1": r'./RAWS/20 STYLES/BOARD 1.png',
                              "BOARD 2": r'./RAWS/20 STYLES/BOARD 2.png',
                              "BOARD 3": r'./RAWS/20 STYLES/BOARD 3.png',
                              "BOARD 4": r'./RAWS/20 STYLES/BOARD 4.png', }

        view = MySelectView(ctx, file_paths, len(splitedte))

        splitedte = splitedte[:limit]
        splitedcd = splitedcd[:limit]
        splitedpos = splitedpos[:limit]
        splitedkill = splitedkill[:limit]
        splitedtotal = splitedtotal[:limit]

        if ctx.message.guild.id in pguilds:
            embed3 = discord.Embed(
                title='**CHOOSE AN OPTION**', color=BotColours.main())
            # await embed_msg.edit(embed=embed3)
        else:
            embed3 = discord.Embed(
                title='**CHOOSE AN OPTION**', color=BotColours.main())
        await embed_msg.edit(embed=embed3, view=view)

        if Titlecolor == "no":
            colors = {"BOARD 1": r'#25e4d4',
                      "BOARD 2": r'#ff5500', "BOARD 3": r'#ff0000', "BOARD 4": r'#22e77a'}
        else:
            for filepath in filepaths:
                colors[ntpath.basename(filepath)[:-4]] = rf"{Titlecolor}"
            # colors = {"BOARD 1": r'#ffe953'}
        server_nname = ctx.message.guild.name
        server_name = ''
        for i in server_nname:
            if i.isalnum():
                server_name += i
        server_name = server_name[:5]
        # try:
        #     await msg.delete()
        #     msg = await self.client.wait_for("message", timeout=15, check=check)
        # except asyncio.TimeoutError:
        #     embed = discord.Embed(
        #         title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=BotColours.error())
        #     await ctx.send(embed=embed)
        #     return
        res = await view.wait()
        if res:
            embed = discord.Embed(
                title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=BotColours.error())
            await embed_msg.edit(embed=embed)
            return
        reply = view.value
        # await msg.delete()
        embed4 = discord.Embed(
            description="**Please Wait <a:icon_loading:939409269978177546>**", color=BotColours.main())
        await embed_msg.edit(embed=embed4)
        try:
            fontsFolder = rf'./FONTS'
            TitleFont1 = ImageFont.truetype(
                os.path.join(fontsFolder, 'Moonrising.ttf'), 139)
            TitleFont2 = ImageFont.truetype(
                os.path.join(fontsFolder, 'Moonrising.ttf'), 67)
            TitleFont3 = ImageFont.truetype(
                os.path.join(fontsFolder, 'league-gothic.leaguegothic-italic.otf'), 139)
            TitleFont4 = ImageFont.truetype(
                os.path.join(fontsFolder, 'league-gothic.leaguegothic-italic.otf'), 80)
            TextFont1 = ImageFont.truetype(
                os.path.join(fontsFolder, 'Retroica.ttf'), 25)

            thing = functools.partial(
                openingFile, file_paths, reply, server_name)
            draw, here = await self.client.loop.run_in_executor(None, thing)
            thing = functools.partial(making_board, here, draw, TextFont1,
                                      splitedte, splitedcd, splitedpos, splitedkill, splitedtotal, custominput)
            embed5 = discord.Embed(
                title="**Done <a:icon_done:939411770458640425>**", color=BotColours.main())
            file = await self.client.loop.run_in_executor(None, thing)
            embed5.set_image(
                url=rf"attachment://{server_name}BOARD1-RESULT.png")

            await ctx.send(embed=embed5, file=file)
            await embed_msg.delete()

            # file = discord.File(rf'./RESULTS/{server_name}BOARD1-RESULT.png')
            # os.remove(rf'./RESULTS/{server_name}BOARD1-RESULT.png')
            # os.remove(rf"./COPIES/{server_name}here.png")

        except Exception as e:
            etype = type(e)
            trace = e.__traceback__
            lines = traceback.format_exception(etype, e, trace)
            traceback_text = ''.join(lines)
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{traceback_text}', color=BotColours.error())
            embed.set_footer(text='Besure To Have Atleast 2')
            await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Leaderboard(client))
