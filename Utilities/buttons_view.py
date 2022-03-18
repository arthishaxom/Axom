from discord.ui import Button, View
import discord
from discord.ext import commands


class MyView(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def button_callback(self, button, interaction):
        await interaction.response.edit_message(view=self)
        self.value = "Yes"
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def no_button_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(view=self)
        self.value = "No"
        self.stop()

    async def on_timeout(self):
        return


class CusView(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="A", style=discord.ButtonStyle.grey)
    async def button_callback(self, button, interaction):
        await interaction.response.edit_message(view=self)
        self.value = "A"
        self.stop()

    @discord.ui.button(label="B", style=discord.ButtonStyle.grey)
    async def no_button_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(view=self)
        self.value = "B"
        self.stop()

    @discord.ui.button(label="C", style=discord.ButtonStyle.grey)
    async def no_button_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(view=self)
        self.value = "C"
        self.stop()

    @discord.ui.button(label="D", style=discord.ButtonStyle.grey)
    async def no_button_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(view=self)
        self.value = "D"
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
