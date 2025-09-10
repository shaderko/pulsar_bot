from discord.ext import commands, tasks
from mongoengine import connect
from models.models import Member
import os
import logging
import discord
from datetime import time
from config import config

logger = logging.getLogger(__name__)

connect(host=os.getenv("MONGO_URL"))


class BirthdayEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(time=time(hour=10, minute=0, second=0))
    async def wish_happy_birthday(self):
        for user in self.bot.get_all_members():
            if user.bot:
                continue

            member = Member.objects.get(uid=user.id)
            if not member.birthday:
                continue

            logger.info(f"Wishing happy birthday for {user.name}")
            if (
                member.birthday.month == discord.utils.utcnow().month
                and member.birthday.day == discord.utils.utcnow().day
            ):
                await self.bot.get_channel(config.birthday_channel).send(
                    f"Happy birthday, {user.mention}! You're now {
                        discord.utils.utcnow().year - member.birthday.year} years old! 🥳"
                )

    @commands.Cog.listener()
    async def on_ready(self):
        self.wish_happy_birthday.start()


def setup(bot):
    bot.add_cog(BirthdayEvents(bot))
