from click import command
import discord
from discord.ext import commands
from Utilities.BotColoursInfo import BotColours
from Utilities.Links import InviteLink, VoteLink


class LinkView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label='Invite Me', url=InviteLink()))
        self.add_item(discord.ui.Button(label='Vote Me', url=VoteLink()))


class AxomHelp(commands.MinimalHelpCommand):

    def get_command_signature(self, command):
        return command.qualified_name

    def get_syntax(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        view = LinkView()
        embed = discord.Embed(title="Axom Help Section",
                              color=BotColours.main())
        embed.set_footer(text="Made With ❤️ | By AE・ARTHISHᵍᶠˣ#2716")
        cog_commands_dict = {}
        for cog, commands in mapping.items():
            cog_name = getattr(cog, "qualified_name", "No Category")
            if cog_name == "AxomHelpCog":
                continue
            filtered = await self.filter_commands(commands, sort=False)
            command_signatures = [
                self.get_command_signature(c) for c in filtered]
            command
            if "serverlist" in command_signatures:
                command_signatures.remove("serverlist")
            if "leave" in command_signatures:
                command_signatures.remove("leave")
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                CommandsNames = "`, `".join(
                    command_signatures)
                cog_commands_dict[cog_name] = CommandsNames

        key_order = ["Leaderboard", "Points", "TourneyHelpers", "Misc"]
        emoji_order = {"Leaderboard": "<:leaderb:947178467156430868>", "Points": "<:icon_usage:947347839518920714>",
                       "TourneyHelpers": "<:awardicon:954265063907283005>", "Misc": "<:box:947178898553204736>"}
        cog_commands_dict = {k: cog_commands_dict[k]
                             for k in key_order if k in cog_commands_dict}
        for cog_name, commands in cog_commands_dict.items():
            embed.add_field(
                name=f"{emoji_order[cog_name]} {cog_name}", value=f"**`{commands}`**", inline=False)

        embed.add_field(name='<:icon_link:947337569299996712> Useful Links', value=f'''
**<:support:947181084863520858> | [Support Server](https://discord.gg/uW7WXxBtBW)
<:bot:947181167990423562> | [Invite The Bot]({InviteLink()})
<:like:947180731656994866> | [Vote Me]({VoteLink()})
**
''')

        channel = self.get_destination()
        await channel.send(embed=embed, view=view)

    async def send_command_help(self, command):
        CmdName = (command.qualified_name).upper()
        embed = discord.Embed(title=CmdName,
                              description=f">>> **{command.help}**", color=BotColours.main())
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
