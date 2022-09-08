import disnake
import pytest
from disnake.ext import commands

from causar import Causar


@pytest.fixture
def causar() -> Causar:
    bot = commands.InteractionBot()

    @bot.slash_command()
    async def interaction_send(inter: disnake.ApplicationCommandInteraction):
        await inter.send("Pong!")
        await inter.send("Second message!")
        await inter.send("Third message!")

    return Causar(bot)
