import discord
import os
from discord.ext import commands
from discord.commands import Option, slash_command
from config import config
from mongoengine import connect
from models.models import Member
import logging
from datetime import date
from discord.commands import slash_command

logger = logging.getLogger(__name__)

connect(host=os.getenv("MONGO_URL"))


class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="set_birthday",
        description="Set up your birthday.",
        guild_ids=config.guild_ids,
    )
    async def set_birthday(
        self,
        ctx: discord.ApplicationContext,
        day: Option(int, "Day of your birthday", min_value=1, max_value=31),
        month: Option(int, "Month of your birthday", min_value=1, max_value=12),
        year: Option(int, "Year of your birthday", min_value=1900),
    ):
        user = ctx.author

        member = Member.objects.get(uid=user.id)

        member.birthday = date(year, month, day)
        member.save()

        await ctx.respond("Your birthday has been successfully set 🎉", ephemeral=True)

    @slash_command(
        name="show_birthday",
        description="Show your birthday.",
        guild_ids=config.guild_ids,
    )
    async def show_birthday(self, ctx: discord.ApplicationContext):
        user = ctx.author

        member = Member.objects.get(uid=user.id)

        await ctx.respond(
            f"Your birthday is on {member.birthday.strftime('%d.%m.%Y')}",
            ephemeral=True,
        )

    @slash_command(
        name="show_birthdays",
        description="Show all birthdays.",
        guild_ids=config.guild_ids,
    )
    async def show_birthdays(self, ctx: discord.ApplicationContext):
        members = Member.objects()

        embed = discord.Embed(
            title="--------- Birthdays ---------",
            description="Birthdays of all members",
            color=discord.Color.purple(),
        )

        for member in members:
            if not member.birthday:
                continue

            user = await self.bot.fetch_user(member.uid)
            embed.add_field(
                name=f"{user.name}",
                value=f"{member.birthday.strftime('%d.%m.%Y')}",
                inline=False,
            )

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Birthday(bot))
