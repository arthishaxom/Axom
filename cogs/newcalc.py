import discord
from discord.ui import Button,View
from discord.ext import commands
import asyncio
import os
import pandas as pd
import csv

class MyView(View):
    def __init__(self,ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None
    @discord.ui.button(label="Yes",style=discord.ButtonStyle.green)
    async def button_callback(self,button,interaction):
        await interaction.response.edit_message(view=self)
        self.value = "Yes"
        self.stop()
    
    @discord.ui.button(label="No",style=discord.ButtonStyle.red)
    async def no_button_callback(self,button,interaction):
        self.clear_items()
        await interaction.response.edit_message(view=self)
        self.value = "No"
        self.stop()
    async def on_timeout(self):
        return

class newcalc(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(name='ncalculate', aliases=['ncalc'],case_insensitive = True)
    @commands.bot_has_permissions(manage_messages = True,embed_links = True)
    @commands.check_any(commands.has_permissions(manage_messages=True),commands.has_role('PT-Mod'),commands.is_owner())
    async def ncalculate(self,ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel


        embed1=discord.Embed(description='''
**You Need The Following Both Formats To Use This Command Properly**

<:px_no1:938969002401730561> Team Prefixes Format
<:px_no2:938969171742588988> Match Points Format

> <a:red:938971541662761001> Info About Both The Formats Are Given Below.
> <a:red:938971541662761001> Use `&slotlist` To Get The Empty Formats.
        ''',color = discord.Colour.gold())
        embed1.add_field(name="<:icon_supp:938970921702678548> TEAM PREFIXES FORMAT",value='''
`Slot-No-1,Team-1-Prefix,Team-Name-1
Slot-No-2,Team-2-Prefix,Team-Name-2`

__Example__ : 
`01,ax,TEAM AXOM
02,ke,KILLER ESPORTS
03,ae,ACOLYTE ESPORTS`
> <a:red:938971541662761001> You Will Have To Use These Prefixes While Inputing Points.
> <a:red:938971541662761001> Use Small Letters In Prefixes Or Else It Will Give Wrong Results.
''')    
        embed1.add_field(name="<:icon_supp:938970921702678548> MATCH RANKS, TEAM PREFIXES & KILLS",value='''
        
`Position-1,Team-Prefix-1,kills
Position-2,Team-Prefix-2,kills`

__Example__ : 
`1,axom,5`
`2,ke,10`
> <a:red:938971541662761001> Here '1' Means The Team Has Got #1 & 'axom' Is The Team Prefix For TEAM AXOM.
> <a:red:938971541662761001> Use Small Letters In Prefixes Or Else It Will Give Wrong Results.
''')
#1ST MATCH
        embed_msg = await ctx.send(embed=embed1)

        ques_embed = discord.Embed(title = "Are You Ready With The Formats?",color = discord.Colour.gold())
        view = MyView(ctx)
        ques_embed = await ctx.send(embed = ques_embed,view=view)

        res = await view.wait()
        if res:
            view.clear_items()
            error_embed = discord.Embed(title = f'Timeout !!!',color = discord.Colour.red())
            await ques_embed.edit(embed=error_embed,view=view)
            return
        if view.value == "No":
            view.clear_items()
            no_embed = discord.Embed(title = "OK, Try Again When You Are Ready",color = discord.Colour.gold())
            await ques_embed.edit(embed = no_embed,view=view)
            return

        await ques_embed.delete()
        if view.value == "Yes":
            embed2 = discord.Embed(title = "SEND FORMATS",description = "Send The First Format With Team Names & Prefixes.",color = discord.Colour.gold())
            await embed_msg.edit(embed=embed2)
            try:
                msg = await self.client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                embed = discord.Embed(title = f'TIMEOUT !!!',description = f'Reply Faster Next Time',color = discord.Colour.red())
                await ctx.send(embed = embed)
                return
            try:
                datas1=msg.content
                split1=datas1.splitlines()
                split1lst = ",".join(split1)
                split2 = split1lst.split(",")
                preteam = {split2[i+1].lower(): split2[i+2] for i in range(0,len(split2),3)}
                await msg.add_reaction("✅")
                await asyncio.sleep(1)
            except Exception as e:
                embed = discord.Embed(title = f'SOME ERROR OCCURED !!!',description = f'The Error : {e}',color = discord.Colour.red())
                await ctx.send(embed = embed)
                await msg.add_reaction("❌")
                return


            listpre = list(preteam)

            await msg.delete()
            embed3 = discord.Embed(title = "NUMBER OF MATCHES",description = "Send The Number Of Matches.",color = discord.Colour.gold())
            await embed_msg.edit(embed=embed3)
            try:
                nmatches_raw = await self.client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                embed = discord.Embed(title = f'TIMEOUT !!!',description = f'Reply Faster Next Time',color = discord.Colour.red())
                await ctx.send(embed = embed)
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
                embed4 = discord.Embed(title = "ENTER MATCH POINTS",description = f"Send The Points Of The Match {i+1} As Per Format.",color = discord.Colour.gold())
                await embed_msg.edit(embed = embed4)
                try:
                    msg = await self.client.wait_for("message", timeout=120, check=check)
                except asyncio.TimeoutError:
                    embed = discord.Embed(title = f'TIMEOUT !!!',description = f'Reply Faster Next Time',color = discord.Colour.red())
                    await ctx.send(embed = embed)
                    return
                
                datas=msg.content
        
                try:
                    column_names = ['teamprefix',f'teamname',f'position{i+1}',f'kills{i+1}',f"cd{i+1}"]
                    with open(f"{server_name}match{i+1}.csv","w+") as csvf:
                        csvw = csv.writer(csvf)
                        csvw.writerow(column_names)
                    df = pd.read_csv(f"{server_name}match{i+1}.csv")


                    dta1=datas.splitlines()
                    dta1join = ",".join(dta1)
                    dta1list = dta1join.split(",")
                    for x in range(len(listpre)):
                        if listpre[x] not in dta1list:
                            dta1list.append('20')
                            dta1list.append(listpre[x])
                            dta1list.append('0')

                    mainlist = []
                    for x in range(0,len(dta1list),3):
                        templ = dta1list[x:x+3]
                        templj = ",".join(templ)
                        mainlist.append(templj)
                    
                    mainlist2 = ";".join(mainlist)

                    dta1=mainlist2.split(";")

                    for x in range(len(dta1)):
                        dtal = dta1[x]
                        dta2 = dtal.split(",")
                        macd = {1:1,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0,24:0,25:0}
                        mapos = {1:15,2:12,3:10,4:8,5:6,6:4,7:2,8:1,9:1,10:1,11:1,12:1,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0,24:0,25:0}
                        df.loc[x]=[dta2[1],preteam[str(dta2[1]).lower()],mapos[int(dta2[0])],int(dta2[2]),macd[int(dta2[0])]]

                    df.to_csv(f"{server_name}match{i+1}.csv",index=False)
                    await msg.add_reaction("✅")
                    await asyncio.sleep(1)
                    await msg.delete()
                except Exception as e:
                    await msg.add_reaction("❌")
                    embed = discord.Embed(title = f'SOME ERROR OCCURED !!!',description = f'The Error : \n{e}',color = discord.Colour.red())
                    await ctx.send(embed = embed)
                    for i in range(nmatches):
                        os.remove(f"{server_name}match{i+1}.csv")
                    return
            

            embed5 = discord.Embed(title = "**RESULTS FORMAT**",description = f'''
**` 1 ` TOP 25
` 2 ` TOP 20
` 3 ` ALL TEAMS**
''',color = discord.Colour.gold())
            
            await embed_msg.edit(embed=embed5)
            try:
                wait_msg = await self.client.wait_for("message", timeout=120, check=check)
                msg = wait_msg.content
                msg = int(msg)
            except Exception as e:
                await msg.add_reaction("❌")
                embed = discord.Embed(title = f'SOME ERROR OCCURED !!!',description = f'The Error : \n{e}',color = discord.Colour.red())
                await ctx.send(embed = embed)
                for i in range(nmatches):
                    os.remove(f"{server_name}match{i+1}.csv")
                return
            await wait_msg.delete()
            result_format = {1:25,2:20}

            col_total = []
            col_position = []
            col_kills = []
            col_wwcd = []
            try:
                if nmatches == 1:
                    df1 = pd.read_csv(f"{server_name}match1.csv")
                    col_to_sum = ['position1','kills1']
                    df1["total1"] = df1[col_to_sum].sum(axis=1)
                    df1.sort_values(by=["total1","cd1","position1","kills1"],ascending=False,inplace=True)
                    
                if nmatches == 2:
                    df1 = pd.read_csv(f"{server_name}match1.csv")
                    df2 = pd.read_csv(f"{server_name}match2.csv")
                    df_total = pd.merge(df1,df2,on=["teamprefix","teamname"],how="inner")
                    for i in range(nmatches):
                        col_total.append(f"position{i+1}")
                        col_total.append(f"kills{i+1}")

                        col_position.append(f"position{i+1}")
                        col_kills.append(f"kills{i+1}")
                        col_wwcd.append(f"cd{i+1}")

                    df_total["total_pts"] = df_total[col_total].sum(axis=1)
                    df_total["total_position"] = df_total[col_position].sum(axis=1)
                    df_total["total_kills"] = df_total[col_kills].sum(axis=1)
                    df_total["total_wwcd"] = df_total[col_wwcd].sum(axis=1)

                    df_total.sort_values(by=["total_pts","total_position","total_wwcd","total_kills"],ascending=False,inplace=True)
                
                if nmatches > 2:
                    df1 = pd.read_csv(f"{server_name}match1.csv")
                    df2 = pd.read_csv(f"{server_name}match2.csv")
                    df_total = pd.merge(df1,df2,on=["teamprefix","teamname"],how="inner")
                    for i in range(nmatches-2):
                        df1 = pd.read_csv(f"{server_name}match{i+3}.csv")
                        df_total=pd.merge(df_total,df1,on=["teamprefix","teamname"],how="inner")
                    for i in range(nmatches):
                        col_total.append(f"position{i+1}")
                        col_total.append(f"kills{i+1}")

                        col_position.append(f"position{i+1}")
                        col_kills.append(f"kills{i+1}")
                        col_wwcd.append(f"cd{i+1}")

                    df_total["total_pts"] = df_total[col_total].sum(axis=1)
                    df_total["total_position"] = df_total[col_position].sum(axis=1)
                    df_total["total_kills"] = df_total[col_kills].sum(axis=1)
                    df_total["total_wwcd"] = df_total[col_wwcd].sum(axis=1)

                    df_total.sort_values(by=["total_pts","total_position","total_wwcd","total_kills"],ascending=False,inplace=True)
            except Exception as e:
                embed = discord.Embed(title = f'SOME ERROR OCCURED !!!',description = f'The Error : \n{e}',color = discord.Colour.red())
                await ctx.send(embed = embed)
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

                    if msg in [1,2]:
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

                    if msg in [1,2]:
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
                embed = discord.Embed(title = f'SOME ERROR OCCURED !!!',description = f'The Error : \n{e}',color = discord.Colour.red())
                await ctx.send(embed = embed)
                for i in range(nmatches):
                    os.remove(f"{server_name}match{i+1}.csv")
                return
            embed6 = discord.Embed(description = f'{valteamsl}\n{valcdsl}\n{valpossl}\n{valkillrsl}\n{valtotalsl}',color = discord.Colour.gold())
            embed6.set_footer(text = "HOLD TO COPY | USE &lb TO LEADERBOARD")
            await embed_msg.edit(embed = embed6)
            for i in range(nmatches):
                os.remove(f"{server_name}match{i+1}.csv")
    



        
            

def setup(client):
    client.add_cog(newcalc(client))