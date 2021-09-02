from os import environ

from nextcord.ext.commands import Context, check


STAFF = int(environ["ADMIN_ROLE"])


def is_admin():
    async def predicate(ctx: Context) -> bool:
        if not ctx.guild: return False

        return STAFF in ctx.author._roles  # type: ignore
    return check(predicate)
