from causar import Causar, Injection, TransactionTypes
from causar.transactions import MessageSent


async def test_basic_bot(causar: Causar):
    injection: Injection = await causar.generate_injection("ping")
    await causar.run_command(injection)

    assert len(injection.transactions) == 2

    transaction: MessageSent = injection.transactions[0]
    assert transaction.type is TransactionTypes.MESSAGE_SENT
    assert transaction.content == "Pong!"

    transaction_2: MessageSent = injection.transactions[1]
    assert transaction_2.type is TransactionTypes.MESSAGE_SENT
    assert transaction_2.content == "Second message!"
