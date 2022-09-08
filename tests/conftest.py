import disnake
import pytest
from disnake.ext import commands

from causar import Causar


@pytest.fixture
def causar() -> Causar:
    bot = commands.InteractionBot()

    @bot.slash_command()
    async def command_one(inter: disnake.ApplicationCommandInteraction):
        await inter.send("Pong!")
        await inter.send("Second message!")
        await inter.send("Third message!")

    @bot.slash_command()
    async def command_two(
        inter: disnake.ApplicationCommandInteraction,
        channel_id: int,
    ):
        channel = await bot.fetch_channel(channel_id)
        await channel.send("Hello!")
        await inter.send("Check the channel you mentioned!", ephemeral=True)

    return Causar(bot)
