import disnake
import pytest
from disnake.ext import commands

from causar import Causar, Injection, TransactionTypes
from causar.transactions import FetchChannel, MessageSent, InteractionResponseSent


async def test_fetch_and_send_to_channel(causar: Causar):
    injection: Injection = await causar.generate_injection("command_two")
    injection.set_kwargs(channel_id=123456789)
    try:
        await causar.run_command(injection)
    except commands.CommandInvokeError as e:
        assert isinstance(e.original, disnake.NotFound)
    else:
        raise RuntimeError("Expected disnake.NotFound")

    assert len(injection.transactions) == 0


async def test_fetch_and_send_to_channel_correct(causar: Causar):
    injection: Injection = await causar.generate_injection("command_two")
    injection.set_kwargs(channel_id=123456789)
    # Populate cache
    causar.cache.add_channel(
        causar.faker.generate_channel(channel_id=123456789),
        injection,
    )
    await causar.run_command(injection)

    assert len(injection.transactions) == 3

    transaction: FetchChannel = injection.transactions[0]
    assert transaction.type is TransactionTypes.FETCH_CHANNEL
    assert transaction.channel_id == 123456789

    transaction_2: MessageSent = injection.transactions[1]
    assert transaction_2.type is TransactionTypes.MESSAGE_SENT
    assert transaction_2.content == "Hello!"

    transaction_3: InteractionResponseSent = injection.transactions[2]
    assert transaction_3.type is TransactionTypes.INTERACTION_RESPONSE_SENT
    assert transaction_3.content == "Check the channel you mentioned!"
    assert transaction_3.ephemeral is True
