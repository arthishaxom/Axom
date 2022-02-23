import discord
from discord.ext import commands

class errors(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_command_error(self,ctx:commands.Context,error:commands.CommandError):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send(f"Be Sure That You Have The Following Permissions: \n`{error.missing_permissions}` OR Have The `PT-Mod` Role")
            return
        elif isinstance(error,commands.BotMissingPermissions):
            await ctx.send(f"Be Sure That I Have The Following Permissions: \n`{error.missing_permissions}`")
            return
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(f"You Missed A Required Argument: \n`{error.param}`")
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error,commands.NotOwner):
            await ctx.send("Sorry To Break Your Heart But This Command Is Owner Only.")
        elif isinstance(error,commands.MaxConcurrencyReached):
            await ctx.send("Bot Is Quite Busy,Try Again In 10-15 Seconds") 
        else:
            print(f"{str(error)}")

    


def setup(client):
    client.add_cog(errors(client))