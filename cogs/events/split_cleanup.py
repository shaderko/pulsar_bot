from discord.ext import commands
from config import config


class SplitCleanup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:
            return

        if (
            config.split_prefix in before.channel.name
            and after.channel != before.channel
            and len(before.channel.members) == 0
        ):
            await before.channel.delete(reason="Split System")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if channel.category is not None and len(channel.category.channels) == 0:
            await channel.category.delete()


def setup(bot):
    bot.add_cog(SplitCleanup(bot))

