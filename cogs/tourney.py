import discord
import asyncio
from discord.ext import commands
from Utilities.buttons_view import MyView
from discord.ui import Button, View
from Utilities.BotColoursInfo import BotColours
from discord.ext.commands.cooldowns import BucketType
from Utilities.cooldownfunc import bypass_for_owner
import typing
# embed_kills = discord.Embed(
#     title=f"<:icon_usage:947347839518920714> What Is `{self.view.value}` Kills?", color=BotColours.main())
# # self.disabled = True
# self.view.clear_items()
# await interaction.response.edit_message(embed=embed_kills, view=self.view)
# self.view.stop()


class SaveButton(Button):
    def __init__(self):
        super().__init__(label=f"Save & Post",
                         style=discord.ButtonStyle.green)

    async def callback(self, interaction):
        self.view.value = "save"
        self.view.clear_items()
        await interaction.response.edit_message(view=self.view)
        self.view.stop()


class DiscardButton(Button):
    def __init__(self):
        super().__init__(label=f"Discard",
                         style=discord.ButtonStyle.red)

    async def callback(self, interaction):
        self.view.value = "discard"
        self.view.clear_items()
        await interaction.response.edit_message(view=self.view)
        self.view.stop()


class MySelectView(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None
        self.add_item(SaveButton())
        self.add_item(DiscardButton())

    async def interaction_check(self, interaction: discord.Interaction):
        if self.ctx.author.id != interaction.user.id:
            return await interaction.response.send_message(content=f"You can't do that! Only {self.ctx.author.mention} can do that!", ephemeral=True)
        return True

    async def on_timeout(self):
        return


class TourneyHelpers(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="tourneychannels", aliases=["tchannels", "tc"], case_insensitive=True, help="Quickly Create Tourney channels")
    @commands.bot_has_permissions(manage_roles=True, manage_permissions=True, manage_channels=True, manage_messages=True, embed_links=True)
    # @commands.dynamic_cooldown(bypass_for_owner, BucketType.guild)
    @commands.dynamic_cooldown(bypass_for_owner, commands.BucketType.guild)
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=False)
    @commands.check_any(commands.has_permissions(manage_channels=True), commands.is_owner())
    async def tourneychannels(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        view = MyView(ctx)
        embed1 = discord.Embed(
            title="<:warning:946654059715244033> CAUTION", description=f"**Before Using This Command, Besure {self.client.user.mention} Is Whitelisted From Any Antinuke Bots, Or Else Boom...Bot Gone\nAre You Ready ?**", color=BotColours.main())
        embed_ques = await ctx.send(embed=embed1, view=view)

        res = await view.wait()
        if res:
            view.clear_items()
            error_embed = discord.Embed(
                title=f'Timeout !!!', color=BotColours.error())
            await embed_ques.edit(embed=error_embed, view=view)
            return
        if view.value == "No":
            view.clear_items()
            no_embed = discord.Embed(
                title="I Won't Be Able To Proceed Without It.", color=BotColours.error())
            await embed_ques.edit(embed=no_embed, view=view)
            return
        if view.value == "Yes":
            view.clear_items()
            # yes_embed = discord.Embed(
            #     title="Please Wait <a:icon_loading:939409269978177546>", color=BotColours.main())
            await embed_ques.edit(view=view)

        embed2 = discord.Embed(
            title="<:icon_usage:947347839518920714> What Is Tournament Name?", color=BotColours.main())
        await embed_ques.edit(embed=embed2)

        try:
            tname = await self.client.wait_for("message", timeout=120, check=check)
            tcname = tname.content
        except asyncio.TimeoutError:
            await tname.delete()
            timeup_embed = discord.Embed(
                title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
            await embed_ques.edit(embed=timeup_embed)
            return
        await tname.delete()

        yes_embed = discord.Embed(
            title="Please Wait <a:icon_loading:939409269978177546>", color=BotColours.main())
        await embed_ques.edit(embed=yes_embed)

        guild = ctx.guild
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, connect=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(manage_channels=True, read_messages=True, send_messages=True,
                                                  attach_files=True, embed_links=True, connect=True, read_message_history=True)
        }
        category = await guild.create_category(f"{tcname}", overwrites=overwrites)
        tcategory = category

        ques_embed = discord.Embed(title=f"<:stary:946641691752935454> Half-Way There <a:icon_loading:939409269978177546>",
                                   description=f"Go To The Category Settings Of the Category Just Created ` [Will Be At Last] ` & Turn On <:turn_on:946698850901577789> The `Manage Permissions` For {self.client.user.mention}.\n> Press **Yes** Button After You Have Done It.", color=BotColours.main())
        view = MyView(ctx)
        ques_embed = await embed_ques.edit(embed=ques_embed, view=view)

        tcname_list = tcname.split()
        if len(tcname_list) > 1:
            tc_list = []
            for i in range(len(tcname_list)):
                e = tcname_list[i][:1]
                tc_list.append(e)
            tcname = "".join(tc_list)
        else:
            tcname = tcname_list[0][:2]

        res = await view.wait()
        if res:
            view.clear_items()
            error_embed = discord.Embed(
                title=f'Timeout !!!', color=BotColours.error())
            await tcategory.edit(embed=error_embed, view=view)
            return
        if view.value == "No":
            view.clear_items()
            no_embed = discord.Embed(
                title="I Won't Be Able To Proceed Without It.", color=BotColours.error())
            await ques_embed.edit(embed=no_embed, view=view)
            await tcategory.delete()
            return
        if view.value == "Yes":
            view.clear_items()
            yes_embed = discord.Embed(
                title="Please Wait <a:icon_loading:939409269978177546>", color=discord.Colour.green())
            await ques_embed.edit(embed=yes_embed, view=view)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, connect=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(manage_channels=True, read_messages=True,
                                                  attach_files=True, embed_links=True, send_messages=True, connect=True, read_message_history=True)
        }
        # overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, connect=True, read_message_history=True),guild.me: discord.PermissionOverwrite(manage_permissions=True, manage_channels=True, read_messages=True,attach_files=True, embed_links=True, send_messages=True, connect=True, read_message_history=True)}
        try:
            await guild.create_text_channel(f"{tcname}_info", category=tcategory, overwrites=overwrites)
            await guild.create_text_channel(f"{tcname}_updates", category=tcategory, overwrites=overwrites)
            await guild.create_text_channel(f"{tcname}_register", category=tcategory, overwrites=overwrites)
            await guild.create_text_channel(f"{tcname}_confirmed", category=tcategory, overwrites=overwrites)
            queriesc = await guild.create_text_channel(f"{tcname}_queries", category=tcategory, overwrites=overwrites)
            await guild.create_voice_channel(f"{tcname}_help-desk", category=tcategory, overwrites=overwrites)

            perms = queriesc.overwrites_for(ctx.guild.default_role)
            perms.send_messages = True
            await queriesc.set_permissions(ctx.guild.default_role, overwrite=perms)

            comp_embed = discord.Embed(
                title="Completed <:tick:946641197642956830>", color=BotColours.main())
            await embed_ques.edit(embed=comp_embed)
        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=BotColours.error())
            await ctx.send(embed=embed)
            raise e
            return

    @commands.command(name="tourneydelete", aliases=["tdelete", "td"], case_insensitive=True, help="Deletes The Channel Of A Category")
    @commands.bot_has_permissions(manage_permissions=True, manage_channels=True, manage_messages=True)
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=False)
    @commands.dynamic_cooldown(bypass_for_owner, commands.BucketType.guild)
    @commands.check_any(commands.has_permissions(manage_channels=True), commands.is_owner())
    async def tourneydelete(self, ctx, *, category: typing.Optional[discord.CategoryChannel] = "invalid"):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        if category == "invalid":
            await ctx.send("**<:iconwarning:946654059715244033> Please Give A Valid Category ID/Name.**")
            return
        ques_embed = discord.Embed(title="<:delete:946641398269083709> You Sure Want To Delete These?",
                                   description="This Category & Every Channel Under This Category Will Be Deleted.", color=BotColours.main())
        view = MyView(ctx)
        ques_embed = await ctx.send(embed=ques_embed, view=view)

        res = await view.wait()
        if res:
            view.clear_items()
            error_embed = discord.Embed(
                title=f'Timeout !!!', color=BotColours.error())
            await ques_embed.edit(embed=error_embed, view=view)
            return
        if view.value == "No":
            view.clear_items()
            no_embed = discord.Embed(title="OK", color=BotColours.main())
            await ques_embed.edit(embed=no_embed, view=view)
            return
        if view.value == "Yes":
            view.clear_items()
            yes_embed = discord.Embed(
                title="Please Wait <a:icon_loading:939409269978177546>", color=BotColours.main())
            await ques_embed.edit(embed=yes_embed, view=view)

        delcategory = category
        channels = delcategory.channels
        try:
            for channel in channels:
                try:
                    await channel.delete()
                except AttributeError:
                    pass
            await delcategory.delete()
            comp_embed = discord.Embed(
                title="Completed <:tick:946641197642956830>", color=BotColours.main())
            await ques_embed.edit(embed=comp_embed)
        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=BotColours.error())
            await ctx.send(embed=embed)
            return

    @commands.command(name="tourneyunhide", aliases=["tunhide", "tuh"], case_insensitive=True, help="Unhides The Channels Of A Category")
    @commands.bot_has_permissions(manage_channels=True)
    @commands.dynamic_cooldown(bypass_for_owner, commands.BucketType.guild)
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=False)
    @commands.check_any(commands.has_permissions(manage_channels=True), commands.is_owner())
    async def tourneyunhide(self, ctx, *, category: typing.Optional[discord.CategoryChannel] = "invalid"):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        if category == "invalid":
            await ctx.send("**<:iconwarning:946654059715244033> Please Give A Valid Category ID/Name.**")
            return
        ques_embed = discord.Embed(title="<:delete:946641398269083709> You Sure Want To Unhide These?",
                                   description="This Category & Every Channel Under This Category Will Be Visible To Everyone.", color=BotColours.main())
        view = MyView(ctx)
        ques_embed = await ctx.send(embed=ques_embed, view=view)

        res = await view.wait()
        if res:
            view.clear_items()
            error_embed = discord.Embed(
                title=f'Timeout !!!', color=BotColours.error())
            await ques_embed.edit(embed=error_embed, view=view)
            return
        if view.value == "No":
            view.clear_items()
            no_embed = discord.Embed(title="OK", color=BotColours.main())
            await ques_embed.edit(embed=no_embed, view=view)
            return
        if view.value == "Yes":
            view.clear_items()
            yes_embed = discord.Embed(
                title="Please Wait <a:icon_loading:939409269978177546>", color=BotColours.main())
            await ques_embed.edit(embed=yes_embed, view=view)

        delcategory = category
        channels = delcategory.channels
        try:
            for channel in channels:
                try:
                    perms = channel.overwrites_for(ctx.guild.default_role)
                    perms.read_messages = True
                    await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
                except AttributeError:
                    pass
            comp_embed = discord.Embed(
                title="Completed <:tick:946641197642956830>", color=BotColours.main())
            await ques_embed.edit(embed=comp_embed)
        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=BotColours.error())
            await ctx.send(embed=embed)
            return

    # @commands.cooldown(1, 60, commands.BucketType.default)
    @commands.command(name="tourneyhide", aliases=["thide", "th"], case_insensitive=True, help="Hides The Channels Of A Category")
    @commands.bot_has_permissions(manage_channels=True)
    @commands.dynamic_cooldown(bypass_for_owner, commands.BucketType.guild)
    @commands.max_concurrency(5, per=commands.BucketType.default, wait=False)
    @commands.check_any(commands.has_permissions(manage_channels=True), commands.is_owner())
    async def tourneyhide(self, ctx, *, category: typing.Optional[discord.CategoryChannel] = "invalid"):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        if category == "invalid":
            await ctx.send("**<:iconwarning:946654059715244033> Please Give A Valid Category ID/Name.**")
            return
        load_embed = discord.Embed(
            title="Please Wait <a:icon_loading:939409269978177546>", color=BotColours.main())
        sent_embed = await ctx.send(embed=load_embed)

        delcategory = category
        channels = delcategory.channels
        try:
            for channel in channels:
                try:
                    perms = channel.overwrites_for(ctx.guild.default_role)
                    perms.read_messages = False
                    await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
                except AttributeError:
                    pass
            comp_embed = discord.Embed(
                title="Completed <:tick:946641197642956830>", color=BotColours.main())
            await sent_embed.edit(embed=comp_embed)
        except Exception as e:
            embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                  description=f'The Error : \n{e}', color=BotColours.error())
            await sent_embed.edit(embed=embed)
            return

    @commands.command(name="tourneyinfo", aliases=["tinfo", "ti"], case_insensitive=True, help="make & Send The Info Of A Tournament To A Channel")
    @commands.bot_has_permissions(manage_messages=True, embed_links=True, manage_webhooks=True)
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    async def tourneyinfo(self, ctx):
        # // category: discord.CategoryChannel
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        # // delcategory = category
        # // channels = delcategory.channels
        # todo ASKING TOURNEY NAME
        ques_embed = discord.Embed(
            title="<:icon_usage:947347839518920714> What Is Tournament's Name ?", color=BotColours.main())
        ques_embed1 = await ctx.send(embed=ques_embed)

        try:
            msg = await self.client.wait_for("message", timeout=100, check=check)
        except asyncio.TimeoutError:
            timeup_embed = discord.Embed(
                title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
            await ques_embed1.edit(embed=timeup_embed)
            return

        tname = (msg.content).upper()
        await msg.delete()

        # todo ASKING TOUNEY PP
        ques2_embed = discord.Embed(
            title="<:icon_usage:947347839518920714> What Is Tournament's PrizePool ?", color=BotColours.main())
        await ques_embed1.edit(embed=ques2_embed)

        try:
            msg = await self.client.wait_for("message", timeout=100, check=check)
        except asyncio.TimeoutError:
            timeup_embed = discord.Embed(
                title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
            await ques_embed1.edit(embed=timeup_embed)
            return

        tprizepool = msg.content
        await msg.delete()

        # todo ASKING TOUNEY PP DISTRIBUTION
        ques2_embed = discord.Embed(
            title="<:icon_usage:947347839518920714> What Is PrizePool Distribution [Upto 10th] ?", description='''
>>> **Write The Distribution Separated By Commas ","
If Some Prize Is Alloted to MVP, Write `mvp` With It.
Example - ` 2000,1000,500,500mvp `**
''', color=BotColours.main())
        await ques_embed1.edit(embed=ques2_embed)

        try:
            msg = await self.client.wait_for("message", timeout=100, check=check)
        except asyncio.TimeoutError:
            timeup_embed = discord.Embed(
                title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
            await ques_embed1.edit(embed=timeup_embed)
            return

        tppdis = msg.content
        tppdis = tppdis.split(",")
        tppdis_forstring = []
        for i in range(len(tppdis)):
            item = tppdis[i].lower()
            pplist = ["1ST - ", "2ND - ", "3RD - ",
                      "4TH - ", "5TH - ", "6TH - ", "7TH - ", "8TH - ", "9TH - ", "10TH - "]
            if "mvp" not in item:
                item = pplist[i] + item
                tppdis_forstring.append(item)
            if "mvp" in item:
                item = item.replace("mvp", "")
                item = "MVP - "+item
                tppdis_forstring.append(item)

        tppdis_string = "\n".join(tppdis_forstring)

        await msg.delete()

        # todo ASKING TOURNEY SLOTS
        ques3_embed = discord.Embed(
            title="<:icon_usage:947347839518920714> What Are The Number Of Slots In The Tournament ?", color=BotColours.main())
        await ques_embed1.edit(embed=ques3_embed)

        try:
            msg = await self.client.wait_for("message", timeout=100, check=check)
        except asyncio.TimeoutError:
            timeup_embed = discord.Embed(
                title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
            await ques_embed1.edit(embed=timeup_embed)
            return

        tslots = msg.content
        await msg.delete()

        # todo ASKING TOURNEY SPONSER
        view = MyView(ctx)

        ques3_embed = discord.Embed(
            title="<:icon_usage:947347839518920714> Does This Tournament Have Different Sponsers ?", color=BotColours.main())
        await ques_embed1.edit(embed=ques3_embed, view=view)
        # ques_embed = await ctx.send(embed=ques_embed, view=view)

        res = await view.wait()
        if res:
            view.clear_items()
            error_embed = discord.Embed(
                title=f'Timeout !!!', color=BotColours.error())
            await ques_embed1.edit(embed=error_embed, view=view)
            return
        if view.value == "No":
            view.clear_items()
            no_embed = discord.Embed(title="OK", color=BotColours.main())
            await ques_embed1.edit(embed=no_embed, view=view)
            spon_name = ctx.guild.name
        if view.value == "Yes":
            view.clear_items()
            yes_embed = discord.Embed(
                title="Ok, Tell What's Their Name?", color=BotColours.main())
            await ques_embed1.edit(embed=yes_embed, view=view)

            try:
                msg = await self.client.wait_for("message", timeout=100, check=check)
                spon_name = msg.content
            except asyncio.TimeoutError:
                await msg.delete()
                timeup_embed = discord.Embed(
                    title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
                await ques_embed1.edit(embed=timeup_embed)
                return
            await msg.delete()

        # todo ASKING TOURNEY BANNER
        view = MyView(ctx)

        ques4_embed = discord.Embed(
            title="<:icon_usage:947347839518920714> Do You Have Any Banner ?", color=BotColours.main())
        await ques_embed1.edit(embed=ques4_embed, view=view)
        # ques_embed = await ctx.send(embed=ques_embed, view=view)

        res = await view.wait()
        if res:
            view.clear_items()
            error_embed = discord.Embed(
                title=f'Timeout !!!', color=BotColours.error())
            await ques_embed1.edit(embed=error_embed, view=view)
            return
        if view.value == "No":
            view.clear_items()
            no_embed = discord.Embed(title="OK", color=BotColours.main())
            await ques_embed1.edit(embed=no_embed, view=view)
            tbanner = ''
        if view.value == "Yes":
            view.clear_items()
            yes_embed = discord.Embed(
                title="Ok, Send It", color=BotColours.main())
            await ques_embed1.edit(embed=yes_embed, view=view)

            try:
                msg = await self.client.wait_for("message", timeout=100, check=check)
                try:
                    tbanner = msg.attachments[0].url
                except:
                    tbanner = msg.content
            except asyncio.TimeoutError:
                timeup_embed = discord.Embed(
                    title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
                await ques_embed1.edit(embed=timeup_embed)
                return
            await msg.delete()

        # todo ASKING TOURNEY EXTRA INFO

        ques4_embed = discord.Embed(
            title="<:icon_usage:947347839518920714> Send Some Extra Info For Your Tournament.", description="**Send Only One-Line Info Like This,\n> MODE : TPP | SQUAD**", color=BotColours.main())
        await ques_embed1.edit(embed=ques4_embed)
        # ques_embed = await ctx.send(embed=ques_embed, view=view)
        try:
            msg = await self.client.wait_for("message", timeout=100, check=check)
            extra_line = msg.content
        except asyncio.TimeoutError:
            timeup_embed = discord.Embed(
                title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
            await ques_embed1.edit(embed=timeup_embed)
            return
        await msg.delete()

        # todo ASKING CHANNEL MENTION
        ques4_embed = discord.Embed(
            title="<:icon_usage:947347839518920714> Where Should I Send This ?", description=f"Mention The Channel, Like This {ctx.channel.mention}", color=BotColours.main())
        await ques_embed1.edit(embed=ques4_embed)

        try:
            msg = await self.client.wait_for("message", timeout=100, check=check)
        except asyncio.TimeoutError:
            timeup_embed = discord.Embed(
                title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
            await ques_embed1.edit(embed=timeup_embed)
            return

        # todo GETTING CHANNEL ID
        try:
            info_channel = self.client.get_channel(msg.channel_mentions[0].id)
        except:
            error_embed = discord.Embed(
                title="Couldn't Find The Channel <:warning:946654059715244033>", color=BotColours.main())
            await ques_embed1.edit(embed=error_embed)
        # // guildiff = self.client.get_guild(856034795863932978)
        await msg.delete()
        # todo GETTING SERVER INFO
        guild_name = ctx.guild.name
        if ctx.guild.icon == None:
            guild_avatar = self.client.user.display_avatar.url
        else:
            guild_avatar = ctx.guild.icon.url
        # guild_avatar = ctx.guild.icon.url

        # // async with aiohttp.ClientSession() as session:
        # //     async with session.get(guild_avatar) as raw:
        # //         guild_avatarBytes = io.BytesIO(await raw.content.read())
        # // await ctx.send(file=discord.File(guild_avatarBytes, "Guild.png"))
        # ////  , avatar=guild_avatarBytes
        # todo WEBHOOK CREATION AND TO INFO CHANNEL
        try:
            tinfo_webhook = await info_channel.create_webhook(name=f"{guild_name}_ti", reason="Tourney Info")
            # <a:ani_crown:951433548114579477> {tname} <a:ani_crown:951433548114579477>
            string = tname.center(26, "ㅤ")
            tinfo_embed = discord.Embed(description=f'''
<:award_icon:954244984960327690> ━━━━━━━━━ <a:ani_crown:951433548114579477> ━━━━━━━━ <:award_icon:954244984960327690>
**{string}**
<:award_icon:954244984960327690> ━━━━━━━━━ <a:ani_crown:951433548114579477> ━━━━━━━━ <:award_icon:954244984960327690>

**<:line_top:947143646334042122> Presented By - {guild_name}
<:line_middle:947143807525326868> Sponsored By - {spon_name}
<:line_middle:947143807525326868> PrizePool - {tprizepool}
<:line_middle:947143807525326868> Total Slots - {tslots}
<:line_bottom:947143905810473050> {extra_line}**
''', color=BotColours.main())
            # tinfo_embed.set_thumbnail(url=ticon)
            tinfo_embed.set_image(url=tbanner)

            tinfo_embed.add_field(
                name="<:icon_money:951122302001635368> PrizePool Distribution", value=f"**{tppdis_string}**", inline=False)
            await tinfo_webhook.send(username=f"{guild_name}", avatar_url=f"{guild_avatar}", embed=tinfo_embed)

            success_embed = discord.Embed(
                title="Sent The Info <:tick:946641197642956830>", color=BotColours.main())
            await ques_embed1.edit(embed=success_embed)
            await tinfo_webhook.delete()
        except:
            error_embed = discord.Embed(
                title="<:iconwarning:946654059715244033> No Permissions In the Mentioned Channel", color=BotColours.error())
            await ctx.send(embed=error_embed)

    @ commands.command(name="tourneyinfo2", aliases=["tinfo2", "t2"], case_insensitive=True, help="make & Send The Info Of A Tournament To A Channel")
    @ commands.bot_has_permissions(manage_messages=True, embed_links=True)
    @ commands.check_any(commands.has_permissions(manage_messages=True), commands.is_owner())
    async def tourneyinfo2(self, ctx):
        # // category: discord.CategoryChannel
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        TournamentPresenter = ctx.guild.name
        TournamentName = "Tournament Name"
        TournamentPP = "0000"
        TournamentPPDis = "0000,000"
        TournamentSlots = "0000"

        Main_Embed = discord.Embed(
            title="Tournament Info Preview", description=f'''
<:award_icon:954244984960327690> ━━━━━━━━━ <a:ani_crown:951433548114579477> ━━━━━━━━ <:award_icon:954244984960327690>
**__{TournamentName}__**
<:award_icon:954244984960327690> ━━━━━━━━━ <a:ani_crown:951433548114579477> ━━━━━━━━ <:award_icon:954244984960327690>
<:line_top:947143646334042122> Presented By - {TournamentPresenter}
<:line_middle:947143807525326868> Sponsored By - {TournamentPresenter}
<:line_middle:947143807525326868> PrizePool - {TournamentPP}
<:line_middle:947143807525326868> Total Slots - {TournamentSlots}
''', color=BotColours.main())

        view = MySelectView(ctx)
        MainMsg = await ctx.send(content=f"Sending This To {ctx.channel.mention}", embed=Main_Embed, view=view)

        res = await view.wait()
        if res:
            embed = discord.Embed(
                title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=BotColours.error())
            await ctx.send(embed=embed)
            return
        # while view.value != "discard":
        #     if view.value == "title":
        #         await ctx.send(f"What Is The Name Of The Tournament")
        #         try:
        #             msg = await self.client.wait_for("message", timeout=100, check=check)
        #             TitleVal = msg.content
        #         except asyncio.TimeoutError:
        #             await msg.delete()
        #             timeup_embed = discord.Embed(
        #                 title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
        #             await ctx.send(embed=timeup_embed)
        #             return
        #         Main_Embed.title = TitleVal
        #         await MainMsg.edit(content=f"Sending This To {ctx.channel.mention}", embed=Main_Embed, view=view)


async def setup(client):
    await client.add_cog(TourneyHelpers(client))
