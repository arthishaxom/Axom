from click import command
import discord
from discord.ext import commands
from Utilities.BotColoursInfo import BotColours


class AxomHelp(commands.MinimalHelpCommand):

    def get_command_signature(self, command):
        return command.qualified_name

    def get_syntax(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Axom Help Section",
                              color=BotColours.main())
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=False)
            command_signatures = [
                self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                CommandsNames = "`, `".join(
                    command_signatures)
                embed.add_field(
                    name=f"<:awardicon:954265063907283005> {cog_name}", value=f"\n`{CommandsNames}`\n", inline=False)
        embed.add_field(name='<:icon_link:947337569299996712> Useful Links', value='''
**<:support:947181084863520858> | [Support Server](https://discord.gg/uW7WXxBtBW)
<:bot:947181167990423562> | [Invite The Bot](https://discord.com/api/oauth2/authorize?client_id=908949899645706241&permissions=2952916049&scope=bot%20applications.commands)
<:like:947180731656994866> | [Vote Me](https://top.gg/bot/880314360017338380/vote)
**
''')

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        CmdName = (command.qualified_name).upper()
        embed = discord.Embed(title=CmdName,
                              description=f">>> **{command.help}**")
        embed.add_field(name="<:icon_usage:947347839518920714> Usage",
                        value=f"**```\n{self.get_syntax(command)}\n```**")
        alias = command.aliases
        alias_text = ", ".join(alias)
        if alias:
            embed.add_field(
                name="<:icon_alias:947347903511404555> Aliases", value=f"**```\n{alias_text}\n```**", inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


class AxomHelpCog(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, client):
        self.client = client
        help_command = AxomHelp()
        help_command.cog = self
        client.help_command = help_command


async def setup(client):
    await client.add_cog(AxomHelpCog(client))
