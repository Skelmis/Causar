from __future__ import annotations

import datetime
import random
import string
from functools import partial
from typing import TypeVar

import disnake
from disnake.ext.commands import InteractionBot

from causar import Transaction, transactions

TransactionT = TypeVar("TransactionT", bound=Transaction, covariant=True)


# noinspection PyMethodMayBeStatic
class Injection:
    def __init__(self, bot: InteractionBot, command_name: str):
        self._kwargs = {}
        self._bot: InteractionBot = bot
        self.command_name: str = command_name
        self._transactions: list[TransactionT] = []

    def set_kwargs(self, **kwargs) -> Injection:
        """Set the keyword arguments to call the command with."""
        self._kwargs = kwargs
        return self

    def _generate_b64(self, *, length: int = 214, has_upper=False) -> str:
        # 214 at time of impl
        if not has_upper:
            return "".join(
                random.choices(string.ascii_lowercase + string.digits, k=length)
            )
        else:
            return "".join(
                random.choices(
                    string.ascii_lowercase + string.digits + string.ascii_uppercase,
                    k=length,
                )
            )

    def _deconstruct_snowflake(self, snowflake: int):
        timestamp = (snowflake >> 22) + 1420070400000
        worker = (snowflake & 0x3E0000) >> 17
        process = (snowflake & 0x1F000) >> 12
        increment = snowflake & 0xFFF

        return timestamp, worker, process, increment

    def _generate_snowflake_raw(
        self, timestamp: int, worker: int, process: int, increment: int
    ) -> int:
        """Create a realistic snowflake

        Parameters
        ----------
        timestamp: int
            Milliseconds
        worker: int
            5 bit integer
        process: int
            5 bit integer
        increment: int
            12
        """
        snowflake = (
            ((timestamp - 1420070400000) << 22)
            | (worker << 17)
            | (process << 12)
            | increment
        )
        return snowflake

    def _generate_snowflake(self, timestamp: int | None = None) -> str:
        if timestamp is None:
            timestamp = int(datetime.datetime.now().timestamp())

        return str(
            self._generate_snowflake_raw(
                timestamp=timestamp, worker=16, process=17, increment=12
            )
        )

    def _format_kwargs(self) -> list[dict]:
        opts: list[dict] = []
        for k, v in self._kwargs.items():
            # TODO Improve this
            v_type = 4 if isinstance(v, int) else 3
            opts.append({"name": k, "value": v, "type": v_type})

        return opts

    def as_interaction(self) -> disnake.ApplicationCommandInteraction:
        # TODO Replace with custom guilds, channels etc
        data = {
            "version": 1,
            "type": 2,
            "token": self._generate_b64(has_upper=True),
            "member": {
                "user": {
                    "username": "Skelmis",
                    "public_flags": 256,
                    "id": "271612318947868673",
                    "discriminator": "9135",
                    "avatar_decoration": None,
                    "avatar": self._generate_b64(length=32),
                },
                "roles": [
                    "737533643353751616",
                    "737533859926638642",
                    "806740882463653899",
                ],
                "premium_since": None,
                "permissions": "4398046511103",
                "pending": False,
                "nick": "Ethan",
                "mute": False,
                "joined_at": "2020-09-18T23:14:06.680000+00:00",
                "is_pending": False,
                "flags": 0,
                "deaf": False,
                "communication_disabled_until": None,
                "avatar": None,
            },
            "locale": "en-US",
            "id": "1016666832901517383",
            "guild_locale": "en-US",
            "guild_id": "737166408525283348",
            "data": {
                "type": 1,
                "options": self._format_kwargs(),
                "name": self.command_name,
                "id": self._generate_snowflake(),
                "guild_id": self._generate_snowflake(),
            },
            "channel_id": self._generate_snowflake(),
            "application_id": "846324706389786676",
            "app_permissions": "4398046511103",
        }
        aci: disnake.ApplicationCommandInteraction = (
            disnake.ApplicationCommandInteraction(
                state=self._bot._connection, data=data
            )
        )
        aci.send = partial(
            transactions.MessageSent.construct, transactions=self._transactions
        )
        return aci

    @property
    def transactions(self) -> list[TransactionT]:
        return self._transactions
