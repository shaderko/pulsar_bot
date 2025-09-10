import discord
from discord.ext import commands
from discord.commands import Option, slash_command
from config import config
import random
from itertools import cycle


class Split(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="split",
        description="Split the current voice channel into rooms",
        guild_ids=config.guild_ids,
    )
    async def split(
        self,
        ctx: discord.ApplicationContext,
        number: Option(int, "Number of rooms", min_value=2, max_value=4),
    ):
        channel_users = ctx.author.voice.channel.members
        if number > len(channel_users):
            await ctx.respond(
                "Cannot split: number of rooms is bigger than the number of currently connected users"
            )
            return

        guild = self.bot.get_guild(config.guild_ids[0])
        category = await guild.create_category(f"{config.split_prefix}_ROOMS")
        channels = [
            await guild.create_voice_channel(
                f"{config.split_prefix}_#{i + 1}",
                category=category,
                reason="Split System",
            )
            for i in range(number)
        ]
        random.shuffle(channel_users)
        for user, channel in zip(channel_users, cycle(channels)):
            await user.move_to(channel)
        await ctx.respond("Split rooms created and users moved.")


def setup(bot):
    bot.add_cog(Split(bot))
