import discord
from discord.ui import Button,View
from discord.ext import commands
import asyncio

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


    @commands.command(name='newcalculate', aliases=['ncalc'],case_insensitive = True)
    @commands.bot_has_permissions(manage_messages = True,embed_links = True)
    @commands.check_any(commands.has_permissions(manage_messages=True),commands.has_role('PT-Mod'),commands.is_owner())
    async def newcalculate(self,ctx):
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

            for i in range(nmatches):
                await self.client.db.execute(f"CREATE TABLE IF NOT EXISTS {server_name}match{i+1}({server_name}team{i+1} VARCHAR(255),{server_name}pos{i+1} BIGINT, {server_name}kill{i+1} BIGINT, {server_name}cd{i+1} BIGINT, {server_name}slot{i+1} VARCHAR(255))")

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
                        await self.client.db.execute(f"INSERT INTO {server_name}match{i+1}({server_name}slot{i+1},{server_name}team{i+1},{server_name}pos{i+1},{server_name}kill{i+1},{server_name}cd{i+1}) VALUES($1,$2,$3,$4,$5)",dta2[1],preteam[str(dta2[1]).lower()],mapos[int(dta2[0])],int(dta2[2]),macd[int(dta2[0])])
                    await msg.add_reaction("✅")
                    await asyncio.sleep(1)
                    await msg.delete()
                except Exception as e:
                    await msg.add_reaction("❌")
                    embed = discord.Embed(title = f'SOME ERROR OCCURED !!!',description = f'The Error : \n{e}',color = discord.Colour.red())
                    await ctx.send(embed = embed)
                    for i in range(nmatches):
                        await self.client.db.execute(f"DROP TABLE IF EXISTS {server_name}match{i+1}")
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
                    await self.client.db.execute(f"DROP TABLE IF EXISTS {server_name}match{i+1}")
                return
            await wait_msg.delete()
            result_format = {1:" LIMIT 25",2:" LIMIT 20",3:""}

            cd = f'{server_name}cd1'
            kills = f'{server_name}kill1'
            poss = f'{server_name}pos1'
            joint = f'{server_name}match1'
            for i in range(1,nmatches):
                cd += f' + {server_name}cd{i+1}'
                kills += f' + {server_name}kill{i+1}'
                poss += f' + {server_name}pos{i+1}'
                joint += f' INNER JOIN {server_name}match{i+1} ON {server_name}slot1 = {server_name}slot{i+1}'

            if nmatches == 1:
                teamis = await self.client.db.fetch(f"SELECT {server_name}team1,{server_name}cd1,{server_name}pos1,{server_name}kill1,({server_name}pos1 + {server_name}kill1) AS {server_name}total FROM {server_name}match1 ORDER BY {server_name}total DESC,{server_name}cd1 DESC,{server_name}pos1 DESC, {server_name}kill1 DESC{result_format[msg]}")
                # teamis = await self.client.db.fetchall()
            else:
                teamis = await self.client.db.fetch(f"SELECT {server_name}team1,({cd}) AS {server_name}cdt,({poss}) AS {server_name}post,({kills}) AS {server_name}killt,({poss} + {kills}) AS {server_name}total FROM {joint} ORDER BY {server_name}total DESC,{server_name}cdt DESC,{server_name}post DESC,{server_name}killt DESC{result_format[msg]}")
                # teamis = await self.client.db.fetchall()

            valteams = [record[0] for record in teamis]
            valteamsl = ",".join(valteams)
            valcds = [record[1] for record in teamis]
            valcdc = [str(ele) for ele in valcds]
            valcdsl = ",".join(valcdc)
            valposs = [record[2] for record in teamis]
            valpossc = [str(ele) for ele in valposs]
            valpossl = ",".join(valpossc)
            valkillrs = [record[3] for record in teamis]
            valkillrsc = [str(ele) for ele in valkillrs]
            valkillrsl = ",".join(valkillrsc)
            valtotals = [record[4] for record in teamis]
            valtotalsc = [str(ele) for ele in valtotals]
            valtotalsl = ",".join(valtotalsc)
            embed6 = discord.Embed(description = f'{valteamsl}\n{valcdsl}\n{valpossl}\n{valkillrsl}\n{valtotalsl}',color = discord.Colour.gold())
            embed6.set_footer(text = "HOLD TO COPY | USE &lb TO LEADERBOARD")
            await embed_msg.edit(embed = embed6)
            for i in range(nmatches):
                await self.client.db.execute(f"DROP TABLE IF EXISTS {server_name}match{i+1}")
    
    @commands.command(name = 'nametable',aliases=['nt'])
    @commands.is_owner()
    async def nametable(self, ctx,*,serverid = 856152785880088587):

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        server = self.client.get_guild(int(serverid))

        server_nname = server.name
        server_name = ''
        for i in server_nname:
            if i.isalnum():
                server_name += i

        table_nums = 0
        tables = await self.client.db.fetch('''
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
        ''')
        table_names = []
        for i in tables:
            table_names.append(i)
            table_nums+=1
        table_names = "\n".join([str(i) for i in table_names])
        embed = discord.Embed(title = f'{server_nname}',description=f'''
>>> **Server Name : {server_nname}
{table_names}
This Much Only**
''')
        await ctx.send(embed=embed)
        if len(table_names) >= 1:
            await ctx.send("`Wanna Delete These?`")
            response = await self.client.wait_for("message", timeout=120, check=check)
            response = response.content
            if response.lower() in ['yes','y']:
                for i in range(table_nums):
                    await self.client.db.execute(f"DROP TABLE IF EXISTS {server_name}match{i+1}")
                    await self.client.db.execute(f"DROP TABLE IF EXISTS match{i+1}")
                await ctx.send("DONE")
            else:
                await ctx.send("OK")
        else:
            return
    


        
            

def setup(client):
    client.add_cog(newcalc(client))