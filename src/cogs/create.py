from asyncio import sleep

from nextcord import Embed, ButtonStyle, Interaction, Button, Role, Guild, Member, AllowedMentions
from nextcord.ext.commands import Bot, Cog, Context, command
from nextcord.ui import View, button

from ..checks import is_admin
from ..generator import generate_default


class SettingsView(View):
    def __init__(self, author_id: int, role: Role, guild: Guild) -> None:
        self.role = role
        self.guild = guild

        self.author_id = author_id

        super().__init__(timeout=86400)

    @button(label="Give Admin", style=ButtonStyle.green, row=0)  # type: ignore
    async def give_admin(self, _button: Button, interaction: Interaction) -> None:
        member = interaction.guild.get_member(interaction.user.id)
        await member.add_roles(self.role)

        await interaction.response.send_message("You now have the admin role.", ephemeral=True)

    @button(label="Revoke Admin", style=ButtonStyle.green, row=0)  # type: ignore
    async def revoke_admin(self, _button: Button, interaction: Interaction) -> None:
        member = interaction.guild.get_member(interaction.user.id)
        await member.remove_roles(self.role)

        await interaction.response.send_message("You no longer have the admin role.", ephemeral=True)

    @button(label="Delete Guild", style=ButtonStyle.green, row=0)  # type: ignore
    async def delete_guild(self, _button: Button, interaction: Interaction) -> None:
        if interaction.user.id != self.author_id:  # type: ignore
            await interaction.response.send_message("You are not authorized to perform this action.", ephemeral=True)
            return

        await interaction.response.send_message("The guild will be deleted shortly.", ephemeral=True)

        await sleep(3)

        await self.guild.delete()


class Create(Cog):
    """A cog for creating servers."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="new")
    @is_admin()
    async def new(self, ctx: Context) -> None:
        """Create a new server."""

        guild, channel, role = await generate_default(ctx.bot, ctx)
        view = SettingsView(ctx.author.id, role, guild)

        embed = Embed(
            colour=0x87CEEB,
            title="NextBox",
            description=(
                "This guild is a sandbox testing guild managed by NextBox.\n"
                "You may assign yourself administrator using the buttons below.\n"
                f"This sandbox was created by **{ctx.author}** <t:{round(guild.created_at.timestamp())}:R>"
            )
        )

        await channel.send(embed=embed, view=view)

        invite = await channel.create_invite()

        await ctx.author.send(f"Sandbox created! {invite.url}")

        await ctx.reply("A sandbox guild has been created and the invite sent to your DMs.", allowed_mentions=AllowedMentions(replied_user=False))


def setup(bot: Bot) -> None:
    """Set up the create cog."""

    bot.add_cog(Create(bot))
