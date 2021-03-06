from typing import Tuple

from nextcord import TextChannel, Permissions, Role, Guild
from nextcord.ext.commands import Bot, Context


with open("nextbox.png", "rb") as f:
    ICON = f.read()


async def generate_default(bot: Bot, ctx: Context) -> Tuple[Guild, TextChannel, Role]:
    guild = await bot.create_guild(name="NextBox Sandbox", code="q7RRmVrncqvv", icon=ICON)

    channels = await guild.fetch_channels()
    for channel in channels:
        await channel.delete()

    cat = await guild.create_category_channel(name="NextBox")
    role = await guild.create_role(name="Administrator", permissions=Permissions(administrator=True))
    channel = await cat.create_text_channel(name="general")

    return (guild, channel, role)
