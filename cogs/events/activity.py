from discord import utils, ActivityType
from discord.ext import commands, tasks
from config import config
from mongoengine import connect
from models.models import Game, Member
import os
import logging

logger = logging.getLogger(__name__)

connect(host=os.getenv("MONGO_URL"))


class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def game_time(self, user):
        if user.activity and user.activity.type == ActivityType.playing:
            activity = user.activity
            all_games = Game.objects(gid=activity.application_id)
            if not all_games:
                game = Game(gid=activity.application_id, name=activity.name)
                game.save()

            member = Member.objects.get(uid=user.id)
            if not member.games:
                member.games = {}

            member.games[str(activity.application_id)] = (
                member.games.get(str(activity.application_id), 0) + 5
            )

            member.save()

    @tasks.loop(minutes=5.0)
    async def active(self):
        active_list = []
        levels = self.bot.get_cog("Levels")
        guild = utils.get(self.bot.guilds, id=config.guild_ids[0])

        for channel in guild.voice_channels:
            channel_members = [
                user
                for user in channel.members
                if not user.bot
                and not user.voice.self_mute
                and not user.voice.self_deaf
            ]
            if len(channel_members) > 1:
                active_list.extend(channel_members)

        counter = 0
        for user in active_list:
            # TODO game object has no attribute activity ID
            # self.game_time(user)
            await levels.add_xp_helper(user, config.active_xp)
            counter += 1

        if counter > 0:
            logger.info(
                f"Performed active bonus XP additon and game recognition for {
                    counter} users."
            )

    @tasks.loop(hours=6)
    async def db_add(self):
        levels = self.bot.get_cog("Levels")
        for user in self.bot.get_all_members():
            if not Member.objects(uid=user.id):
                await levels.setup_new_user(user)

    @commands.Cog.listener()
    async def on_member_join(self, user):
        levels = self.bot.get_cog("Levels")
        await levels.setup_new_user(user)

    @commands.Cog.listener()
    async def on_ready(self):
        self.active.start()
        self.db_add.start()


def setup(bot):
    bot.add_cog(Activity(bot))
