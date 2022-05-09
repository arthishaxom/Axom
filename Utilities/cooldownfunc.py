from discord.ext import commands


def bypass_for_owner(message):
    if message.author.id == 315342835283001344:
        return None
    return commands.Cooldown(1, 60)


def bypass_for_owner2(message):
    if message.author.id == 315342835283001344:
        return None
    return commands.Cooldown(2, 60)
