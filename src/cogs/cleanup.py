from nextcord.ext.commands import Bot, Cog, Context, command

from ..checks import is_admin


class Cleanup(Cog):
    """A cog for cleaning up servers."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="cleanup")
    @is_admin()
    async def delete(self, ctx: Context) -> None:
        """Delete all sandbox servers."""

        to_delete = []

        for guild in self.bot.guilds:
            if guild.owner_id == self.bot.user.id:
                to_delete.append(guild)

        for guild in to_delete:
            await guild.delete()

        await ctx.send(f"Deleted {len(to_delete)} guilds.")


def setup(bot: Bot) -> None:
    """Set up the cleanup cog."""

    bot.add_cog(Cleanup(bot))
