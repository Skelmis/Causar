from causar import Causar, Injection, TransactionTypes
from causar.transactions import InteractionResponseSent


async def test_interaction_send(causar: Causar):
    injection: Injection = await causar.generate_injection("ping")
    await causar.run_command(injection)

    assert len(injection.transactions) == 3

    transaction: InteractionResponseSent = injection.transactions[0]
    assert transaction.type is TransactionTypes.INTERACTION_RESPONSE_SENT
    assert transaction.content == "Pong!"

    transaction_2: InteractionResponseSent = injection.transactions[1]
    assert transaction_2.type is TransactionTypes.INTERACTION_FOLLOWUP_SENT
    assert transaction_2.content == "Second message!"

    transaction_3: InteractionResponseSent = injection.transactions[2]
    assert transaction_3.type is TransactionTypes.INTERACTION_FOLLOWUP_SENT
    assert transaction_3.content == "Third message!"
