from os import environ

from dotenv import load_dotenv
from nextcord import Game, Intents
from nextcord.ext.commands import Bot


def main() -> None:
    load_dotenv()

    intents = Intents.default()
    intents.members = True

    bot = Bot(
        command_prefix="::",
        help_command=None,
        intents=intents,
        activity=Game("in my sandbox."),
    )

    bot.load_extension("src.cogs.create")
    bot.load_extension("src.cogs.cleanup")

    bot.run(environ["BOT_TOKEN"])


if __name__ == '__main__':
    main()
