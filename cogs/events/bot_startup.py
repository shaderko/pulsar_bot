from discord.ext import commands
from config import config
import logging
logger = logging.getLogger(__name__)


class BotStartup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'{self.bot.user.name} has connected to your server!')
        await self.bot.change_presence(activity=config.activity)


def setup(bot):
    bot.add_cog(BotStartup(bot))