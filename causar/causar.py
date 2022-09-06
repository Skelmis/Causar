from disnake.ext.commands import InvokableSlashCommand, InteractionBot

from causar import Injection


class Causar:
    def __init__(self, bot: InteractionBot):
        self.bot: InteractionBot = bot

    async def run_command(
        self,
        injection: Injection,
    ):
        """Invoke a command and return a list of transactions which occurred."""
        command: InvokableSlashCommand = self.bot.get_slash_command(
            injection.command_name
        )
        await command.invoke(injection.as_interaction())

    async def generate_injection(self, command_name: str) -> Injection:
        return Injection(self.bot, command_name=command_name)
