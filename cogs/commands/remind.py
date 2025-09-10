import discord
import asyncio
from discord.ext import commands
from discord.commands import Option, slash_command
from config import config


class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="remind",
        description="Remind me after specific time",
        guild_ids=config.guild_ids,
    )
    async def remind(
        self,
        ctx: discord.ApplicationContext,
        thing: Option(str, "What should you be reminded about"),
        time: Option(int, "Choose time for the reminder - default in minutes"),
        unit: Option(
            str,
            "Enter the time unit",
            choices=["seconds", "minutes", "hours"],
            default="minutes",
        ),
    ):
        units = {"seconds": 1, "minutes": 60, "hours": 60 * 60}
        await ctx.respond(
            f'Reminder for "{thing}" will go off in {time} {unit}', ephemeral=True
        )
        await asyncio.sleep(time * units[unit])
        await ctx.author.send(f'Your reminder for "{thing}" is here')


def setup(bot):
    bot.add_cog(Remind(bot))
