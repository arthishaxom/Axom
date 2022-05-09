import discord
from discord.ext import commands
import traceback
import sys
from Utilities.BotColoursInfo import BotColours


class errors(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        # if isinstance(error, commands.MissingPermissions):
        #     await ctx.send(f"Be Sure That You Have The Following Permissions: \n`{error.missing_permissions}` OR Have The `PT-Mod` Role")
        #     return
        if isinstance(error, commands.BotMissingPermissions):
            PermsList = error.missing_permissions
            PermsList = [perm.upper() for perm in PermsList]
            PermText = "`, `".join(PermsList)
            try:
                await ctx.send(f"**<:iconwarning:946654059715244033> Be Sure That I Have The Following Permissions: \n`{PermText}`**")
                return
            except:
                try:
                    await ctx.author.send(
                        f"**<:iconwarning:946654059715244033> I Cannot Send Messages In {ctx.channel.mention}, Be Sure That I Have The Following Permissions : \n`SEND_MESSAGES`,`{PermText}`**")
                except:
                    print('Ignoring exception in command {}:'.format(
                        ctx.command), file=sys.stderr)
                    traceback.print_exception(
                        type(error), error, error.__traceback__, file=sys.stderr)
                    return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"You Missed A Required Argument: \n`{error.param}`")
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.NotOwner):
            await ctx.send("Sorry To Break Your Heart But This Command Is Owner Only.")
            return
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send("Bot Is Quite Busy,Try Again In 1-2 Minutes")
            return
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"This Command Is On Cooldown, Try Again In {round(error.retry_after,2)} Seconds")
            return
        elif isinstance(error, commands.CheckAnyFailure):
            # print(type(str(ctx.command)))
            if str(ctx.command) in ['ptsetup', 'leaderboard', 'calculate1', 'calculate2']:
                PermsList = (error.errors[0]).missing_permissions
                PermsList = [perm.upper() for perm in PermsList]
                PermText = "`, `".join(PermsList)
                embed = discord.Embed(
                    title="<:iconwarning:946654059715244033> You Are Missing Permissions", description=f"**You Do Not Have Permission To Use This Command. Be Sure That You Have The `PT-Mod` Role OR The Following Permissions: \n`{PermText}`**", color=BotColours.error())
                try:
                    await ctx.send(embed=embed)
                except:
                    await ctx.send(f"**You Do Not Have Permission To Use This Command. Be Sure That You Have The `PT-Mod` Role OR The Following Permissions: \n`{PermText}`**")

            else:
                PermsList = (error.errors[0]).missing_permissions
                PermsList = [perm.upper() for perm in PermsList]
                PermText = "`, `".join(PermsList)
                embed = discord.Embed(
                    title="<:iconwarning:946654059715244033> You Are Missiong Perms", description=f"**You Do Not Have Permission To Use This Command. Be Sure That You Have The The Following Permissions: \n`{PermText}`**", color=BotColours.error())
                try:
                    await ctx.send(embed=embed)
                except:
                    await ctx.send(f"<:iconwarning:946654059715244033> **You Do Not Have Permission To Use This Command. Be Sure That You Have The Following Permissions: \n`{PermText}`**")
        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)


async def setup(client):
    await client.add_cog(errors(client))
