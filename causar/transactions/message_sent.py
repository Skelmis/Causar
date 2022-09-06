import disnake

from causar import Transaction, TransactionTypes


class MessageSent(Transaction):
    def __init__(
        self, content: str | None = None, embeds: list[disnake.Embed] = None, **kwargs
    ):
        super().__init__(TransactionTypes.MESSAGE_SENT)
        self.content: str | None = content
        self.embeds: list[disnake.Embed] = embeds if embeds else []
