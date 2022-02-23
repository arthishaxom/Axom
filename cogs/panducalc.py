import discord
from discord import message
from discord.ext import commands

class pcalc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='pcalculate', aliases=['pcalc'])
    @commands.is_owner()
    async def pcalculate(self,ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel


        ebdDB=discord.Embed(description='''
**__YOU NEED TO HAVE THE FOLLOWING FORMATS BEFORE MOVING FORWARD [MAX TEAMS : 25]__
➡️ Format With TEAM PREFIXES & TEAM NAMES
➡️ Format With MATCH RANKS, TEAM PREFIXES & KILLS
__NOTE__ : Both The Formats Are Given Below
**
        ''',color = discord.Colour.gold())
        ebdDB.add_field(name="TEAM PREFIXES & TEAM NAMES",value='''
>>> `<Team1 Prefix>,<Team1 Name>
<Team2 Prefix>,<Team2 Name>`
**Example : **
`AXOM,TEAM AXOM
KE,KILLER ESPORTS
AE,ACOLYTE ESPORTS`
__Note__ : You Will Have To Use These PREFIXES While Inputing Points.
      
''')    
        ebdDB.add_field(name="MATCH RANKS, TEAM PREFIXES & KILLS",value='''
        
>>> **`<POSITION-1>,<TEAM-PREFIX>,<KILLS>
<POSITION-2>,<TEAM-PREFIX>,<KILLS>`
Example : 
`1,AXOM,5`
`2,KE,10`
Here '1' Means The Team Has Got #1 & 'AXOM' Means The Team Prefix Is AXOM.**
        
''')
#1ST MATCH
        ebdDB.set_footer(text='[MAX = 25 TEAMS]')
        await ctx.send(embed=ebdDB)
        await ctx.send("Reply With `Yes` If You Are Ready, Else Type `No`.")
        
        msg = await self.client.wait_for("message", timeout=120, check=check)
        dta = msg.content

        if dta.lower() in ['yes','yep','ok','yus']:
            await ctx.send("**`Send The First Format With Team Names & Prefixes.`**")
            try:
                msg = await self.client.wait_for("message", timeout=120, check=check)
                datas1=msg.content
                split1=datas1.splitlines()
                split1lst = ",".join(split1)
                split2 = split1lst.split(",")
                preteam = {split2[i+1].lower(): split2[i+2] for i in range(0,len(split2),3)}
                await msg.add_reaction("✅")
            except Exception as e:
                embed = discord.Embed(title = f'SOME ERROR OCCURED !!!',description = f'The Error : {e}')
                await ctx.send(embed = embed)
                await msg.add_reaction("❌")
                return


            listpre = list(preteam)

            await ctx.send("**`How Many Matches?`**")
            nmatches_raw = await self.client.wait_for("message", timeout=120, check=check)
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

            async with self.client.db.cursor() as cur:
                for i in range(nmatches):
                    await cur.execute(f"CREATE TABLE IF NOT EXISTS match{i+1}(team{i+1} VARCHAR(255),pos{i+1} BIGINT, kill{i+1} BIGINT, cd{i+1} BIGINT, slot{i+1} VARCHAR(255))")

            for i in range(nmatches):
                await ctx.send(f'**`Now..Send The {i+1} Match Points As Showed In Format Before.`**')
                msg = await self.client.wait_for("message", timeout=120, check=check)
                datas=msg.content

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

                try:
                    for x in range(len(dta1)):
                        dtal = dta1[x]
                        dta2 = dtal.split(",")
                        macd = {1:1,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0,24:0,25:0}
                        mapos = {1:15,2:12,3:10,4:8,5:6,6:4,7:2,8:1,9:1,10:1,11:1,12:1,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0,22:0,23:0,24:0,25:0}
                        async with self.client.db.cursor() as cur:
                            await cur.execute(f"INSERT INTO match{i+1}(slot{i+1},team{i+1},pos{i+1},kill{i+1},cd{i+1}) VALUES(%s,%s,%s,%s,%s)",(dta2[1],preteam[str(dta2[1]).lower()],mapos[int(dta2[0])],int(dta2[2]),macd[int(dta2[0])]))
                    await msg.add_reaction("✅")
                except Exception as e:
                    embed = discord.Embed(title = f'SOME ERROR OCCURED !!!',description = f'The Error : \n{e}')
                    await ctx.send(embed = embed)
                    async with self.client.db.cursor() as cur:
                        for i in range(nmatches):
                            await cur.execute(f"DROP TABLE IF EXISTS match{i+1}")
                    return

            cd = f'cd1'
            kills = f'kill1'
            poss = f'pos1'
            joint = f'match1'
            for i in range(1,nmatches):
                cd += f' + cd{i+1}'
                poss += f' + pos{i+1}'
                kills += f' + kill{i+1}'
                joint += f' INNER JOIN match{i+1} ON slot1 = slot{i+1}'

            async with self.client.db.cursor() as cur:
                if nmatches == 1:
                    await cur.execute(f"SELECT team1,cd1,pos1,kill1,(pos1 + kill1) AS total FROM match1 ORDER BY total DESC,cd1 DESC,pos1 DESC, kill1 DESC")
                    teamis = await cur.fetchall()
                else:
                    await cur.execute(f"SELECT team1,({cd}) AS cdt,({poss}) AS post,({kills}) AS killt,({poss} + {kills}) AS total FROM {joint} ORDER BY total DESC,cdt DESC,post DESC,killt DESC")
                    teamis = await cur.fetchall()

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
            await ctx.send(f'{valteamsl}\n{valcdsl}\n{valpossl}\n{valkillrsl}\n{valtotalsl}')
            async with self.client.db.cursor() as cur:
                for i in range(nmatches):
                    await cur.execute(f"DROP TABLE IF EXISTS match{i+1}")
            await ctx.send("DATA CLEARED")              
        else:
            await ctx.send("**`Try Again When You Are Ready.`**")


        
            

def setup(client):
    client.add_cog(pcalc(client))