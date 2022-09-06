import disnake
import pytest
from disnake.ext import commands

from causar import Causar


@pytest.fixture
def causar() -> Causar:
    bot = commands.InteractionBot()

    @bot.slash_command()
    async def ping(inter: disnake.ApplicationCommandInteraction):
        await inter.send("Pong!")
        await inter.send("Second message!")

    return Causar(bot)
