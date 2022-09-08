from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING, Union
from unittest.mock import Mock

import disnake

from causar import Transaction, transactions, InjectionMetadata, CacheLookupFailed

if TYPE_CHECKING:
    from causar import Causar, Faker, Cache

TransactionT = TypeVar("TransactionT", bound=Transaction, covariant=True)


class Injection:
    def __init__(
        self,
        causar: Causar,
        command_name: str,
        *,
        metadata: InjectionMetadata | None = None,
    ):
        self._kwargs = {}
        self.causar: Causar = causar
        self.command_name: str = command_name
        self.transactions: list[TransactionT] = []

        if not metadata:
            metadata = InjectionMetadata(
                guild_id=self.faker.generate_snowflake(),
                channel_id=self.faker.generate_snowflake(),
            )

        self.metadata: InjectionMetadata = metadata

        self.__has_responded: bool = False

    @property
    def faker(self) -> Faker:
        return self.causar.faker

    @property
    def cache(self) -> Cache:
        return self.causar.cache

    def set_kwargs(self, **kwargs) -> Injection:
        """Set the keyword arguments to call the command with."""
        self._kwargs = kwargs
        return self

    def _format_kwargs(self) -> list[dict]:
        opts: list[dict] = []
        for k, v in self._kwargs.items():
            # TODO Improve this
            v_type = 4 if isinstance(v, int) else 3
            opts.append({"name": k, "value": v, "type": v_type})

        return opts

    def as_interaction(self) -> disnake.ApplicationCommandInteraction:
        self.metadata.command_name = self.command_name
        aci: disnake.ApplicationCommandInteraction = (
            self.causar.faker.generate_interaction(
                kwargs=self._format_kwargs(), metadata=self.metadata
            )
        )
        aci.send = self._send_response_or_followup
        self.causar.bot.fetch_channel = self._inject_fetch_channel
        return aci

    async def _inject_fetch_channel(
        self, channel_id: int
    ) -> Union[
        disnake.abc.GuildChannel,
        disnake.abc.PrivateChannel,
        disnake.abc.Thread,
    ]:
        try:
            channel = self.cache.get_channel(channel_id)
        except CacheLookupFailed:
            raise disnake.NotFound(
                response=Mock(),
                message=f"Failed to find channel {channel_id} in the mock cache.",
            )
        else:
            await transactions.FetchChannel.construct(
                channel_id, transactions=self.transactions
            )
            return channel

    async def _send_response_or_followup(self, *args, **kwargs):
        if self.__has_responded:
            return await transactions.InteractionFollowUpSent.construct(
                *args, transactions=self.transactions, **kwargs
            )

        self.__has_responded = True
        return await transactions.InteractionResponseSent.construct(
            *args, transactions=self.transactions, **kwargs
        )
