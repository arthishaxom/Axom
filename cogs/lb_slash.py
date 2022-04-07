import discord
import os
import asyncio
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from discord.utils import get
from Utilities.helpful_lb import top20, top25
import functools
import io
from Utilities.BotColoursInfo import BotColours
from discord import app_commands
import traceback
from discord.ui import Button, View


class BoardButtons(Button):
    def __init__(self, label):
        super().__init__(label=f"Board {label}",
                         style=discord.ButtonStyle.grey)

    async def callback(self, interaction):
        self.view.value = (self.label).split()[1]
        self.view.clear_items()
        await interaction.response.edit_message(view=self.view)
        self.view.stop()


class MySelectView(View):
    def __init__(self, dicti):
        super().__init__(timeout=60)
        self.value = None
        for i in dicti.keys():
            self.add_item(BoardButtons(i))

    @discord.ui.button(label="Preview", style=discord.ButtonStyle.blurple)
    async def preview_callback(self, interaction, button):
        pic = discord.Embed(title="BOARD 1", color=BotColours.main())
        file = discord.File(r'./PREVS/BOARD-1.png')
        pic.set_image(url='attachment://BOARD-1.png')
        pic2 = discord.Embed(title="BOARD 2", color=BotColours.main())
        file2 = discord.File(r'./PREVS/BOARD-2.png')
        pic2.set_image(url='attachment://BOARD-2.png')
        pic3 = discord.Embed(title="BOARD 3", color=BotColours.main())
        file3 = discord.File(r'./PREVS/BOARD-3.png')
        pic3.set_image(url='attachment://BOARD-3.png')
        await interaction.response.defer()
        await interaction.followup.send(files=[file, file2, file3], embeds=[pic, pic2, pic3], ephemeral=True)

    # @discord.ui.button(label="Board 2", style=discord.ButtonStyle.grey)
    # async def button2_callback(self, interaction, button):
    #     self.value = "2"
    #     self.stop()

    # @discord.ui.button(label="Board 3", style=discord.ButtonStyle.grey)
    # async def button3_callback(self, interaction, button):
    #     self.value = "3"
    #     self.stop()

    # async def interaction_check(self, interaction: discord.Interaction):
    #     if self.interaction.user.id != interaction.user.id:
    #         return await interaction.response.send_message(content=f"You can't do that! Only {self.interaction.user.mention} can do that!", ephemeral=True)
    #     return True

    async def on_timeout(self):
        return


class Feedback(discord.ui.Modal, title='Feedback'):
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
        label='FORMAT',
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

    async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)


class LeaderboardSlash(commands.Cog):

    def __init__(self, client):
        self.client = client

    @app_commands.command(name='preview', description='Preview The Leaderboards')
    @app_commands.checks.bot_has_permissions(embed_links=True)
    @app_commands.guilds(discord.Object(id=856152785880088587), discord.Object(id=746337818388987967))
    # @app_commands.checks.bot_has_permissions(embed_links=True, attach_files=True)
    async def preview(self, interaction: discord.Interaction):
        pic = discord.Embed(title="BOARD 1", color=BotColours.main())
        file = discord.File(r'./PREVS/BOARD-1.png')
        pic.set_image(url='attachment://BOARD-1.png')
        pic2 = discord.Embed(title="BOARD 2", color=BotColours.main())
        file2 = discord.File(r'./PREVS/BOARD-2.png')
        pic2.set_image(url='attachment://BOARD-2.png')
        pic3 = discord.Embed(title="BOARD 3", color=BotColours.main())
        file3 = discord.File(r'./PREVS/BOARD-3.png')
        pic3.set_image(url='attachment://BOARD-3.png')
        await interaction.response.defer()
        await interaction.followup.send(files=[file, file2, file3], embeds=[pic, pic2, pic3])
        # await interaction.followup.send(file=file3, embed=pic3)
        # await ctx.send(file=file2, embed=pic2)
        # await ctx.send(file=file3, embed=pic3)

    # @app_commands.command(name="slash", description="Slash command")
    # @app_commands.guilds(discord.Object(id=856152785880088587))
    # async def slash(self, interaction: discord.Interaction, number: int, string: str):
    #     await interaction.response.send_message(f'{number=} {string=}', ephemeral=True)

    @app_commands.command(name='ptsetup', description="Makes A Role `PT-Mod`.")
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.guilds(discord.Object(id=856152785880088587), discord.Object(id=746337818388987967))
    async def ptsetup(self, interaction: discord.Interaction):
        guilded = interaction.guild
        if get(interaction.guild.roles, name="PT-Mod"):
            await interaction.response.send_message("Role Is Already Created")
            return
        else:
            await guilded.create_role(name="PT-Mod", color=BotColours.main())
            await interaction.response.send_message("Created Role!, Now People With This Role Can Use My Commands Even If They Don't Have Manage_Messages Perms.")

    @app_commands.command(name="leaderboard", description='''Makes The Leaderboards.''')
    @app_commands.checks.bot_has_permissions(manage_messages=True, embed_links=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.guilds(discord.Object(id=856152785880088587), discord.Object(id=746337818388987967))
    # @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    # @commands.bot_has_permissions(manage_messages=True, embed_links=True, attach_files=True)
    # @commands.check_any(commands.has_permissions(manage_messages=True), commands.has_role('PT-Mod'), commands.is_owner())
    async def leaderboard(self, interaction: discord.Interaction):
        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        def openingFile(file_paths, reply, server_name):
            lb = Image.open(f'{file_paths[int(reply)]}').convert('RGBA')

            # copy =
            # copy.save(rf"./COPIES/{server_name}here.png")
            # here = Image.open(rf"./COPIES/{server_name}here.png")
            here = lb.copy()
            draw = ImageDraw.Draw(here)
            return draw, here

        def making_board(here, draw, title, TextFont1, splitedte, splitedcd, splitedpos, splitedkill, splitedtotal, pguilds):

            if interaction.guild.id not in pguilds:
                if len(splitedte) > 20:
                    top25.title(draw, title, TitleFont1,
                                TitleFont2, colors, reply)
                else:
                    top20.title(draw, title, TitleFont1,
                                TitleFont2, colors, reply)
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
            with io.BytesIO() as a:
                here.save(a, "png")
                a.seek(0)
                file = discord.File(
                    a, filename=rf"{server_name}BOARD1-RESULT.png")
            return file

        try:
            #             embed1 = discord.Embed(title='**__SEND FORMAT__**', description='''
            # **```
            # TEAM1,TEAM2,...
            # CHICKEN1,CHICKEN2,...
            # POSITON1,POSTION2,...
            # KILL1,KILL2,...
            # TOTAL1,TOTAL2,...
            # ```**
            # ''', color=BotColours.main())
            #             embed1.set_footer(text='Besure To Have Atleast 2 Teams')
            # embed_msg = await interaction.response.send_message(embed=embed1)

            # msg = await self.client.wait_for("message", timeout=30, check=check)
            feedback_modal = Feedback()
            await interaction.response.send_modal(feedback_modal)
            await feedback_modal.wait()

            # print(feedback_modal.maintitle.value)
            # print(feedback_modal.subtitle.value)
            # print(feedback_modal.maindata.value)
            # main_editable = await interaction.followup.send(f'Ok, Processing Your Leaderboard', ephemeral=True, wait=True)
            title = [feedback_modal.maintitle.value,
                     feedback_modal.subtitle.value]
            data = feedback_modal.maindata.value
            datas = data.splitlines()

        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=BotColours.error())
            await interaction.followup.send(embed=embed)
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
            await interaction.followup.send(embed=embed)
            return

        pguilds = [667103945503670282]
#         if interaction.guild_id not in pguilds:
#             embed2 = discord.Embed(title='**ENTER TITLE & SUBTITLE**', description='''
# > Title,Subitle
# > Example : T3 SCRIMS,XYZ ESPORTS
# <a:red:938971541662761001> Length Of The Titles Should Under 15.
# ''', color=BotColours.main())
#             embed2.set_footer(text='Spaces Are Also Counted.')
#             await msg.delete()
#             await interaction.edit_original_message(embed=embed2)
#             try:
#                 msg = await self.client.wait_for("message", timeout=60, check=check)
#             except asyncio.TimeoutError:
#                 embed = discord.Embed(
#                     title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=BotColours.error())
#                 await interaction.followup.send(embed=embed)
#                 return
#             try:
#                 title = msg.content
#                 title = title.split(",")
#                 print(title)
#             except Exception as e:
#                 embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
#                                       description=f'The Error : \n{e}', color=BotColours.error())
#                 await interaction.followup.send(embed=embed)
#                 return
        if interaction.guild_id in pguilds:
            file_paths = {1: r'./RAWS/T2_AE.png', 2: r'./RAWS/T2Q_AE.png',
                          3: r'./RAWS/VETERAN_AE.png'}
        else:
            if len(splitedte) > 20:
                file_paths = {1: r'./RAWS/BOARD-1_25.png',
                              2: r'./RAWS/BOARD-2_25.png',
                              3: r'./RAWS/BOARD-3_25.png', }
            else:
                file_paths = {1: r'./RAWS/BOARD-1.png',
                              2: r'./RAWS/BOARD-2.png',
                              3: r'./RAWS/BOARD-3.png', }
        view = MySelectView(file_paths)
        if interaction.guild_id in pguilds:
            embed3 = discord.Embed(title='**__CHOOSE AN OPTION__**', description='''
**` 1 ` T2 SCRIMS [ACOLYTE]
` 2 ` T2Q SCRIMS [ACOLYTE]
` 3 ` VETERAN SCRIMS [ACOLYTE]**
''', color=BotColours.main())
            await interaction.followup.send(embed=embed3, view=view)
        else:
            embed3 = discord.Embed(title='**__CHOOSE AN OPTION__**', description='''
**` 1 ` BOARD 1
` 2 ` BOARD 2
` 3 ` BOARD 3**
''', color=BotColours.main())
            main_editable = await interaction.followup.send(embed=embed3, view=view, wait=True)
            # await main_editable.edit(embed=embed3, view=view)

        res = await view.wait()
        if res:
            await interaction.followup.send("wtf dude")
            return
        reply = int(view.value)

        colors = {1: r'#25e4d4', 2: r'#ff5500', 3: r'#ff0000'}

        server_nname = interaction.guild.name
        server_name = ''
        for i in server_nname:
            if i.isalnum():
                server_name += i
        server_name = server_name[:5]

        embed4 = discord.Embed(
            description="**Please Wait <a:icon_loading:939409269978177546>**", color=BotColours.main())
        await main_editable.edit(embed=embed4)

        # try:
        fontsFolder = rf'./FONTS'
        TitleFont1 = ImageFont.truetype(
            os.path.join(fontsFolder, 'Moonrising.ttf'), 139)
        TitleFont2 = ImageFont.truetype(
            os.path.join(fontsFolder, 'Moonrising.ttf'), 67)
        TextFont1 = ImageFont.truetype(
            os.path.join(fontsFolder, 'Retroica.ttf'), 25)

        thing = functools.partial(
            openingFile, file_paths, reply, server_name)
        draw, here = await self.client.loop.run_in_executor(None, thing)
        thing = functools.partial(making_board, here, draw, title, TextFont1,
                                  splitedte, splitedcd, splitedpos, splitedkill, splitedtotal, pguilds)
        embed5 = discord.Embed(
            title="**Done <a:icon_done:939411770458640425>**", color=BotColours.main())
        file = await self.client.loop.run_in_executor(None, thing)
        embed5.set_image(
            url=rf"attachment://{server_name}BOARD1-RESULT.png")

        await interaction.followup.send(embed=embed5, file=file)
        await main_editable.delete()
        # await interaction.response.delete()

        # file = discord.File(rf'./RESULTS/{server_name}BOARD1-RESULT.png')
        # os.remove(rf'./RESULTS/{server_name}BOARD1-RESULT.png')
        # os.remove(rf"./COPIES/{server_name}here.png")

        # except Exception as e:
        #     embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
        #                           description=f'The Error : \n{e}', color=BotColours.error())
        #     embed.set_footer(text='Besure To Have Atleast 2')
        #     await interaction.followup.send(embed=embed)


async def setup(client):
    await client.add_cog(LeaderboardSlash(client))
