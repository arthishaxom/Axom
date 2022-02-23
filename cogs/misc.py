from discord.ui import Button,View
import discord
from discord.ext import commands
import json

import requests


class misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='serverlist',aliases = ['servers','slist'])
    @commands.is_owner()
    async def serverlist(self,ctx):
        serverlist = []
        i = 0
        for guild in self.client.guilds:
            i+=1
            e = f"{str(i)} - {guild.name} : {guild.id}"
            serverlist.append(e)

        button_left = Button(emoji='<:RedLeft:941266906462191626>')
        button_right = Button(emoji='<:RedRight:941266864330408016>')


        view = View()
        view.add_item(button_left)
        view.add_item(button_right)

        total_servers = len(serverlist)
        serverlist = [serverlist[i:i+total_servers//2] for i in range(0,total_servers,total_servers//2)]
        serverlist1 = serverlist[0]
        serverlist2 = serverlist[1]
        serverlist1 = "\n".join(serverlist1)
        serverlist2 = "\n".join(serverlist2)
        embed1 = discord.Embed(title = f"Total Servers : {total_servers}",description = f"{serverlist1}",color = discord.Colour.gold())
        embed2 = discord.Embed(title = f"Total Servers : {total_servers}",description = f"{serverlist2}",color = discord.Colour.gold())
        async def button_callback1(interaction):
            await interaction.response.edit_message(embed = embed2)
        async def button_callback2(interaction):
            await interaction.response.edit_message(embed = embed1)

        button_right.callback = button_callback1
        button_left.callback = button_callback2
        await ctx.send(embed=embed1,view = view)

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f"My Ping : `{round(self.client.latency*1000)}ms` <:icon_ping:938972151510360125>\nThis Means Alive...Right?")

    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx, guild_id):
        await self.client.get_guild(int(guild_id)).leave()
        await ctx.send(f"I left: {guild_id}")

    @commands.command(name ='stats',pass_context = True,case_insensitive = True,aliases = ['st'])
    async def stats(self,ctx):
        url = 'https://panel.epikhost.xyz/api/client/servers/b0b9e335/resources'
        headers = {
            "Authorization": "Bearer vD6wPREn7IcJdMKh0DYu70OPPLZRzpZ7VPfRXWLnLskXtOSC",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.request('GET', url, headers=headers)
        response = json.loads(response.text)
        memory_usage = int(response['attributes']['resources']['memory_bytes'])//1024**2
        disk_usage = int(response['attributes']['resources']['disk_bytes'])//1024**2
        cpu_usage = round(float(response['attributes']['resources']['cpu_absolute']),2)

        member_count = sum(guild.member_count for guild in self.client.guilds)

        embed = discord.Embed(title="AXOM Stats",color = discord.Colour.gold())
        embed.add_field(name="**__Servers Info__**",value = f'''
Total Servers : {len(self.client.guilds)}
Total Users : {member_count}        
''')    
        embed.add_field(name="**__System Stats__**",value = f'''
CPU : {cpu_usage}% Used
RAM : {memory_usage}/500 MB Used
DISK : {disk_usage}/500 MB Used
''')
        embed.set_footer(text = "Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")

        await ctx.send(embed = embed)



def setup(client):
    client.add_cog(misc(client))