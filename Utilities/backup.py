from pipes import Template
import discord
from discord.ui import Button, View
from discord.ext import commands
import asyncio
import os
import pandas as pd
import csv
from Utilities.BotColoursInfo import BotColours


# class DropdownView(discord.ui.View):
#     def __init__(self, teamlist):
#         super().__init__(timeout=5)
#         self.add_item(Dropdown(teamlist))

#     async def on_timeout(self):
#         return
class Dropdown(discord.ui.Select):
    def __init__(self, teamlist):

        # Set the options that will be presented inside the dropdown
        # global options
        options = []
        for i in range(len(teamlist)):
            teamn = teamlist[i]
            teamname = discord.SelectOption(
                label=f'{teamn}')
            options.append(teamname)
        super().__init__(placeholder='Choose your Team',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # opt = discord.utils.get(self.options, label=self.values[0])
        # self.options.remove(opt)
        self.view.value = self.values[0]
        await interaction.message.delete()
        self.view.stop()


class MySelectView(View):
    def __init__(self, ctx, teamlist):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None
        self.add_item(Dropdown(teamlist))

    @discord.ui.button(label="Save", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        await interaction.response.edit_message(view=self)
        self.value = "save"
        self.stop()

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.grey)
    async def no_button_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(view=self)
        self.value = "skip"
        self.stop()

    async def on_timeout(self):
        return


class MyView(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        await interaction.response.edit_message(view=self)
        self.value = "Yes"
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_button_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(view=self)
        self.value = "No"
        self.stop()

    async def on_timeout(self):
        return


class Points(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='calculate1', aliases=["calc1", "c1"], case_insensitive=True, help='''
Quickly Calculate Points Of Unlimited Matches. Use calculate2 If You Are Having Trouble Undersanding The Process.
''')
    @commands.bot_has_permissions(manage_messages=True, embed_links=True)
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.has_role('PT-Mod'), commands.is_owner())
    async def calculate1(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        embed1 = discord.Embed(description='''
**You Need The Following Both Formats To Use This Command Properly**

<:px_no1:938969002401730561> Team Prefixes Format
<:px_no2:938969171742588988> Match Points Format

> <a:red:938971541662761001> Info About Both The Formats Are Given Below.
> <a:red:938971541662761001> Use `&slotlist` To Get The Empty Formats.
        ''', color=discord.Colour.gold())
        embed1.add_field(name="<:icon_supp:938970921702678548> TEAM PREFIXES FORMAT", value='''
`Slot-No-1,Team-1-Prefix,Team-Name-1
Slot-No-2,Team-2-Prefix,Team-Name-2`

__Example__ : 
`01,ax,TEAM AXOM
02,ke,KILLER ESPORTS
03,ae,ACOLYTE ESPORTS`
> <a:red:938971541662761001> You Will Have To Use These Prefixes While Inputing Points.
> <a:red:938971541662761001> Use Small Letters In Prefixes Or Else It Will Give Wrong Results.
''')
        embed1.add_field(name="<:icon_supp:938970921702678548> MATCH RANKS, TEAM PREFIXES & KILLS", value='''
        
`Position-1,Team-Prefix-1,kills
Position-2,Team-Prefix-2,kills`

__Example__ : 
`1,axom,5`
`2,ke,10`
> <a:red:938971541662761001> Here '1' Means The Team Has Got #1 & 'axom' Is The Team Prefix For TEAM AXOM.
> <a:red:938971541662761001> Use Small Letters In Prefixes Or Else It Will Give Wrong Results.
''')
# 1ST MATCH
        embed_msg = await ctx.send(embed=embed1)

        ques_embed = discord.Embed(
            title="Are You Ready With The Formats?", color=discord.Colour.gold())
        view = MyView(ctx)
        ques_embed = await ctx.send(embed=ques_embed, view=view)

        res = await view.wait()
        if res:
            view.clear_items()
            error_embed = discord.Embed(
                title=f'Timeout !!!', color=discord.Colour.red())
            await ques_embed.edit(embed=error_embed, view=view)
            return
        if view.value == "No":
            view.clear_items()
            no_embed = discord.Embed(
                title="OK, Try Again When You Are Ready", color=discord.Colour.gold())
            await ques_embed.edit(embed=no_embed, view=view)
            return

        await ques_embed.delete()
        if view.value == "Yes":
            embed2 = discord.Embed(
                title="SEND FORMATS", description="Send The First Format With Team Names & Prefixes.", color=discord.Colour.gold())
            await embed_msg.edit(embed=embed2)
            try:
                msg = await self.client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=discord.Colour.red())
                await ctx.send(embed=embed)
                return
            try:
                datas1 = msg.content
                split1 = datas1.splitlines()
                split1lst = ",".join(split1)
                split2 = split1lst.split(",")
                preteam = {split2[i+1].lower(): split2[i+2]
                           for i in range(0, len(split2), 3)}
                await msg.add_reaction("✅")
                await asyncio.sleep(1)
            except Exception as e:
                embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                      description=f'The Error : {e}', color=discord.Colour.red())
                await ctx.send(embed=embed)
                await msg.add_reaction("❌")
                return

            listpre = list(preteam)

            await msg.delete()
            embed3 = discord.Embed(
                title="NUMBER OF MATCHES", description="Send The Number Of Matches.", color=discord.Colour.gold())
            await embed_msg.edit(embed=embed3)
            try:
                nmatches_raw = await self.client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=discord.Colour.red())
                await ctx.send(embed=embed)
                return
            try:
                nmatches = int(nmatches_raw.content)
            except Exception as e:
                await ctx.send("`NUMBER BHEJIYE GURUDEV`")
                await nmatches_raw.add_reaction("❌")
                return

            server_nname = ctx.message.guild.name
            server_name = ''
            for i in server_nname:
                if i.isalnum():
                    server_name += i

            await nmatches_raw.delete()
            for i in range(nmatches):
                embed4 = discord.Embed(
                    title="ENTER MATCH POINTS", description=f"Send The Points Of The Match {i+1} As Per Format.", color=discord.Colour.gold())
                await embed_msg.edit(embed=embed4)
                try:
                    msg = await self.client.wait_for("message", timeout=120, check=check)
                except asyncio.TimeoutError:
                    embed = discord.Embed(
                        title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=discord.Colour.red())
                    await ctx.send(embed=embed)
                    return

                datas = msg.content

                try:
                    column_names = ['teamprefix', f'teamname',
                                    f'position{i+1}', f'kills{i+1}', f"cd{i+1}"]
                    with open(f"{server_name}match{i+1}.csv", "w+") as csvf:
                        csvw = csv.writer(csvf)
                        csvw.writerow(column_names)
                    df = pd.read_csv(f"{server_name}match{i+1}.csv")

                    dta1 = datas.splitlines()
                    dta1join = ",".join(dta1)
                    dta1list = dta1join.split(",")
                    for x in range(len(listpre)):
                        if listpre[x] not in dta1list:
                            dta1list.append('20')
                            dta1list.append(listpre[x])
                            dta1list.append('0')

                    mainlist = []
                    for x in range(0, len(dta1list), 3):
                        templ = dta1list[x:x+3]
                        templj = ",".join(templ)
                        mainlist.append(templj)

                    mainlist2 = ";".join(mainlist)

                    dta1 = mainlist2.split(";")

                    for x in range(len(dta1)):
                        dtal = dta1[x]
                        dta2 = dtal.split(",")
                        macd = {1: 1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                                14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0}
                        mapos = {1: 15, 2: 12, 3: 10, 4: 8, 5: 6, 6: 4, 7: 2, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1,
                                 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0}
                        df.loc[x] = [dta2[1], preteam[str(dta2[1]).lower()], mapos[int(
                            dta2[0])], int(dta2[2]), macd[int(dta2[0])]]

                    df.to_csv(f"{server_name}match{i+1}.csv", index=False)
                    await msg.add_reaction("✅")
                    await asyncio.sleep(1)
                    await msg.delete()
                except Exception as e:
                    await msg.add_reaction("❌")
                    embed = discord.Embed(
                        title=f'SOME ERROR OCCURED !!!', description=f'The Error : \n{e}', color=discord.Colour.red())
                    await ctx.send(embed=embed)
                    for i in range(nmatches):
                        os.remove(f"{server_name}match{i+1}.csv")
                    return

            embed5 = discord.Embed(title="**RESULTS FORMAT**", description=f'''
**` 1 ` TOP 25
` 2 ` TOP 20
` 3 ` ALL TEAMS**
''', color=discord.Colour.gold())

            await embed_msg.edit(embed=embed5)
            try:
                wait_msg = await self.client.wait_for("message", timeout=120, check=check)
                msg = wait_msg.content
                msg = int(msg)
            except Exception as e:
                await msg.add_reaction("❌")
                embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                      description=f'The Error : \n{e}', color=discord.Colour.red())
                await ctx.send(embed=embed)
                for i in range(nmatches):
                    os.remove(f"{server_name}match{i+1}.csv")
                return
            await wait_msg.delete()
            result_format = {1: 25, 2: 20}

            col_total = []
            col_position = []
            col_kills = []
            col_wwcd = []
            try:
                if nmatches == 1:
                    df1 = pd.read_csv(f"{server_name}match1.csv")
                    col_to_sum = ['position1', 'kills1']
                    df1["total1"] = df1[col_to_sum].sum(axis=1)
                    df1.sort_values(
                        by=["total1", "cd1", "position1", "kills1"], ascending=False, inplace=True)

                if nmatches == 2:
                    df1 = pd.read_csv(f"{server_name}match1.csv")
                    df2 = pd.read_csv(f"{server_name}match2.csv")
                    df_total = pd.merge(
                        df1, df2, on=["teamprefix", "teamname"], how="inner")
                    for i in range(nmatches):
                        col_total.append(f"position{i+1}")
                        col_total.append(f"kills{i+1}")

                        col_position.append(f"position{i+1}")
                        col_kills.append(f"kills{i+1}")
                        col_wwcd.append(f"cd{i+1}")

                    df_total["total_pts"] = df_total[col_total].sum(axis=1)
                    df_total["total_position"] = df_total[col_position].sum(
                        axis=1)
                    df_total["total_kills"] = df_total[col_kills].sum(axis=1)
                    df_total["total_wwcd"] = df_total[col_wwcd].sum(axis=1)

                    df_total.sort_values(
                        by=["total_pts", "total_position", "total_wwcd", "total_kills"], ascending=False, inplace=True)

                if nmatches > 2:
                    df1 = pd.read_csv(f"{server_name}match1.csv")
                    df2 = pd.read_csv(f"{server_name}match2.csv")
                    df_total = pd.merge(
                        df1, df2, on=["teamprefix", "teamname"], how="inner")
                    for i in range(nmatches-2):
                        df1 = pd.read_csv(f"{server_name}match{i+3}.csv")
                        df_total = pd.merge(df_total, df1, on=[
                                            "teamprefix", "teamname"], how="inner")
                    for i in range(nmatches):
                        col_total.append(f"position{i+1}")
                        col_total.append(f"kills{i+1}")

                        col_position.append(f"position{i+1}")
                        col_kills.append(f"kills{i+1}")
                        col_wwcd.append(f"cd{i+1}")

                    df_total["total_pts"] = df_total[col_total].sum(axis=1)
                    df_total["total_position"] = df_total[col_position].sum(
                        axis=1)
                    df_total["total_kills"] = df_total[col_kills].sum(axis=1)
                    df_total["total_wwcd"] = df_total[col_wwcd].sum(axis=1)

                    df_total.sort_values(
                        by=["total_pts", "total_position", "total_wwcd", "total_kills"], ascending=False, inplace=True)
            except Exception as e:
                embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                      description=f'The Error : \n{e}', color=discord.Colour.red())
                await ctx.send(embed=embed)
                for i in range(nmatches):
                    os.remove(f"{server_name}match{i+1}.csv")
                return

            try:
                if nmatches == 1:
                    valteams = df1["teamname"].to_list()
                    valcds = df1["cd1"].to_list()
                    valposs = df1["position1"].to_list()
                    valkillrs = df1["kills1"].to_list()
                    valtotals = df1["total1"].to_list()

                    if msg in [1, 2]:
                        valteams = valteams[:result_format[msg]]
                        valcds = valcds[:result_format[msg]]
                        valposs = valposs[:result_format[msg]]
                        valkillrs = valkillrs[:result_format[msg]]
                        valtotals = valtotals[:result_format[msg]]

                    valteamsl = ",".join(valteams)
                    valcdc = [str(ele) for ele in valcds]
                    valcdsl = ",".join(valcdc)
                    valpossc = [str(ele) for ele in valposs]
                    valpossl = ",".join(valpossc)
                    valkillrsc = [str(ele) for ele in valkillrs]
                    valkillrsl = ",".join(valkillrsc)
                    valtotalsc = [str(ele) for ele in valtotals]
                    valtotalsl = ",".join(valtotalsc)
                else:
                    valteams = df_total["teamname"].to_list()
                    valcds = df_total["total_wwcd"].to_list()
                    valposs = df_total["total_position"].to_list()
                    valkillrs = df_total["total_kills"].to_list()
                    valtotals = df_total["total_pts"].to_list()

                    if msg in [1, 2]:
                        valteams = valteams[:result_format[msg]]
                        valcds = valcds[:result_format[msg]]
                        valposs = valposs[:result_format[msg]]
                        valkillrs = valkillrs[:result_format[msg]]
                        valtotals = valtotals[:result_format[msg]]

                    valteamsl = ",".join(valteams)
                    valcdc = [str(ele) for ele in valcds]
                    valcdsl = ",".join(valcdc)
                    valpossc = [str(ele) for ele in valposs]
                    valpossl = ",".join(valpossc)
                    valkillrsc = [str(ele) for ele in valkillrs]
                    valkillrsl = ",".join(valkillrsc)
                    valtotalsc = [str(ele) for ele in valtotals]
                    valtotalsl = ",".join(valtotalsc)
            except Exception as e:
                embed = discord.Embed(title=f'SOME ERROR OCCURED !!!',
                                      description=f'The Error : \n{e}', color=discord.Colour.red())
                await ctx.send(embed=embed)
                for i in range(nmatches):
                    os.remove(f"{server_name}match{i+1}.csv")
                return
            embed6 = discord.Embed(
                description=f'{valteamsl}\n{valcdsl}\n{valpossl}\n{valkillrsl}\n{valtotalsl}', color=discord.Colour.gold())
            embed6.set_footer(text="HOLD TO COPY | USE &lb TO LEADERBOARD")
            await embed_msg.edit(embed=embed6)
            for i in range(nmatches):
                os.remove(f"{server_name}match{i+1}.csv")


# TODO Calculate Points Command #2 = c2


    @commands.command(name='calculate2', aliases=["c2", "calc2"], case_insensitive=True, help='''
Does The Same As Calculate1 But Uses Buttons & Selects, A Easier Way For People Who Dont Understand Calculate1 Method
''')
    @commands.bot_has_permissions(manage_messages=True, embed_links=True)
    @commands.check_any(commands.has_permissions(manage_messages=True), commands.has_role('PT-Mod'), commands.is_owner())
    async def calculate2(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        embed3 = discord.Embed(
            title="NUMBER OF MATCHES", description="Send The Number Of Matches.", color=discord.Colour.gold())
        await ctx.send(embed=embed3)
        # try:
        #     NoOfMatchesRaw = await self.client.wait_for("message", timeout=120, check=check)
        # except asyncio.TimeoutError:
        #     await NoOfMatchesRaw.delete()
        #     embed = discord.Embed(
        #         title=f'TIMEOUT !!!', description=f'Reply Faster Next Time', color=discord.Colour.red())
        #     await ctx.send(embed=embed)
        #     return
        # try:
        #     NoOfMatches = int(NoOfMatchesRaw.content)
        # except Exception as e:
        #     await ctx.send("`NUMBER BHEJIYE GURUDEV`")
        #     await NoOfMatchesRaw.add_reaction("❌")
        #     return
        # await NoOfMatchesRaw.delete()

        server_nname = ctx.message.guild.name
        server_name = ''
        for i in server_nname:
            if i.isalnum():
                server_name += i

        AskSlotlistEmbed = discord.Embed(
            title="<:icon_usage:947347839518920714> Send The Slotlist.", color=BotColours.main())
        AskSlotlist = await ctx.send(embed=AskSlotlistEmbed)
        try:
            SlotlistObject = await self.client.wait_for("message", timeout=15, check=check)
            SlotlistRaw = SlotlistObject.content
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title=f'<:icon_error:947347839518920714> Timeout Error. Please Try Again.', color=BotColours.error())
            await AskSlotlist.edit(embed=embed)
            return
        await AskSlotlist.delete()
        await SlotlistObject.delete()
        SlotlistLineSplit = SlotlistRaw.splitlines()
        if '@' in SlotlistLineSplit[0]:
            SlotlistOnly = []
            for Val in SlotlistLineSplit:
                if "@" in Val:
                    ele = i.split("@")
                    SlotlistOnly.append(ele[0])
        else:
            SlotlistOnly = SlotlistLineSplit
        print(SlotlistOnly)
        SlotlistFinal = []
        for i in [')', '=>', '>', '|']:
            for team in SlotlistOnly:
                if i in team:
                    ele = ((team.split(i))[1].strip())
                    SlotlistFinal.append(ele)
        print(SlotlistFinal)
        column_names = [f'teamname',
                        f'position1', f'kills1', f"cd1"]
        with open(f"{server_name}match1.csv", "w+") as csvf:
            csvw = csv.writer(csvf)
            csvw.writerow(column_names)
        df = pd.read_csv(f"{server_name}match1.csv")

        macd = {1: 1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0,
                14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0}
        mapos = {1: 15, 2: 12, 3: 10, 4: 8, 5: 6, 6: 4, 7: 2, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1,
                 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0}

        TeamList = SlotlistFinal
        TeamRank = 1

        for i in range(len(TeamList)):

            embed1 = discord.Embed(
                title=f"<:icon_usage:947347839518920714> Choose The #{TeamRank} Team", color=BotColours.main())
            view = MySelectView(ctx, TeamList)
            MainEmbed = await ctx.send(embed=embed1, view=view)
            res = await view.wait()
            if res:
                view.clear_items()
                error_embed = discord.Embed(
                    title=f'<:icon_error:947347839518920714> Timeout Error. Please Try Again.', color=BotColours.error())
                await MainEmbed.edit(embed=error_embed, view=view)
                return
            if view.value in TeamList:
                try:
                    embed2 = discord.Embed(
                        title=f"<:icon_usage:947347839518920714> What Is `{view.value}` Kills?", color=BotColours.main())
                    embed_obj = await ctx.send(embed=embed2)
                    TeamKillsQues = await self.client.wait_for("message", timeout=60, check=check)
                    TeamKills = int(TeamKillsQues.content)
                    print(view.value)

                    TeamName = view.value
                    TeamPosPts = mapos[TeamRank]
                    TeamKillsPts = TeamKills
                    TeamWwcd = macd[TeamRank]

                    df.loc[i] = [TeamName, TeamPosPts,
                                 TeamKillsPts, TeamWwcd]

                    TeamList.remove(view.value)
                    print(TeamList)
                    TeamRank += 1
                    await TeamKillsQues.delete()
                    await embed_obj.delete()
                except asyncio.TimeoutError:
                    await TeamKillsQues.delete()
                    timeup_embed = discord.Embed(
                        title="Times Up <:icon_clock:947357599030997043>", color=BotColours.error())
                    await ctx.send(embed=timeup_embed)
                    return
            else:
                if view.value == "skip":
                    await MainEmbed.delete()
                    print("skipped")
                    TeamRank += 1
                else:
                    print("Starting With : ", TeamList)
                    await MainEmbed.delete()
                    for i in TeamList:
                        print("Team Added : ", i)
                        df.loc[TeamRank] = [i, 0,
                                            0, 0]
                        # TeamList.remove(i)
                        print(TeamList)
                        TeamRank += 1
                    break

        if TeamList != []:
            for i in TeamList:
                df.loc[TeamRank] = [i, 0, 0, 0]
                TeamRank += 1

        df.to_csv(f"{server_name}match1.csv", index=False)

        df1 = pd.read_csv(f"{server_name}match1.csv")
        col_to_sum = ['position1', 'kills1']
        df1["total1"] = df1[col_to_sum].sum(axis=1)
        df1.sort_values(
            by=["total1", "cd1", "position1", "kills1"], ascending=False, inplace=True)

        valteams = df1["teamname"].to_list()
        valcds = df1["cd1"].to_list()
        valposs = df1["position1"].to_list()
        valkillrs = df1["kills1"].to_list()
        valtotals = df1["total1"].to_list()

        valteamsl = ",".join(valteams)
        valcdc = [str(ele) for ele in valcds]
        valcdsl = ",".join(valcdc)
        valpossc = [str(ele) for ele in valposs]
        valpossl = ",".join(valpossc)
        valkillrsc = [str(ele) for ele in valkillrs]
        valkillrsl = ",".join(valkillrsc)
        valtotalsc = [str(ele) for ele in valtotals]
        valtotalsl = ",".join(valtotalsc)

        embed6 = discord.Embed(
            description=f'{valteamsl}\n{valcdsl}\n{valpossl}\n{valkillrsl}\n{valtotalsl}', color=discord.Colour.gold())
        embed6.set_footer(text="HOLD TO COPY | USE &lb TO LEADERBOARD")
        await ctx.send(embed=embed6)
        os.remove(f"{server_name}match1.csv")


async def setup(client):
    await client.add_cog(Points(client))
    