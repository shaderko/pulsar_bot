import discord
import os
from discord.ext import commands
from discord.commands import Option, slash_command
from config import config
from mongoengine import connect
from models.models import Member
import logging

logger = logging.getLogger(__name__)

connect(host=os.getenv('MONGO_URL'))

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_num_bots(self):
        return len([x for x in self.bot.users if x.bot])

    async def get_status(self, item, value):
        if item == 'latency':
            return '✅' if value < 0.5 else '❌'
        if item == 'database':
            return '✅' if len(value) > 0 else '❌'
        if item == 'cogs':
            return '✅' if value == len(config.startup_extensions) else '❌'
        if item == 'users':
            return '✅' if value[0]>=(value[1]-value[2]) else '❌'
        if item == 'bot_type':
            return '🔓' if value else '🔒'

    @slash_command(name='ping', description='Check bot latency.', guild_ids=config.guild_ids)
    async def ping(self, ctx: discord.ApplicationContext):
        logger.info("Pinging")
        embed = discord.Embed(
            title = '--------- Status ---------',
            description=f'Owner: {(await self.bot.application_info()).owner.mention}',
            color = discord.Color.green()
        )
        bot_public = (await self.bot.application_info()).bot_public
        embed.add_field(name=f'{await self.get_status("bot_type", bot_public)}  |  Bot Type', value=f'{"Public" if bot_public else "Private"}', inline=False)
        latency = self.bot.latency
        embed.add_field(name=f'{await self.get_status("latency", latency)}  |  Latency', value=latency, inline=False)
        members = Member.objects()
        embed.add_field(name=f'{await self.get_status("database", members)}  |  Database', value=f'{"Connected" if len(members) > 0 else "Not connected"}', inline=False)
        cogs = self.bot.cogs
        embed.add_field(name=f'{await self.get_status("cogs", len(cogs))}  |  Cogs', value=f'{len(cogs)}/{len(config.startup_extensions)}', inline=False)
        users = self.bot.users
        bots = await self.get_num_bots()
        embed.add_field(name=f'{await self.get_status("users", (len(members), len(users), bots))}  |  Users', value=f'{len(members)}/{len(users)} ({bots} bots)', inline=False)
        missing = set([user.id for user in users if not user.bot]) - set([member.uid for member in members])
        missing = [(await self.bot.fetch_user(x)).name for x in missing]
        if missing:
            embed.add_field(name=f'Users missing from database:', value=f'{missing}', inline=False)
        await ctx.respond(embed=embed)

    @slash_command(name='wake', description='Gently wakes up an user.', guild_ids=config.guild_ids)
    async def wake(self, ctx: discord.ApplicationContext,
                    user: Option(discord.Member, "Choose a user to wake")):
        channels = (ctx.author.voice.channel, self.bot.get_channel(config.afk_channel))
        current = 1

        if channels[0] is None or user not in channels[0].members:
            await ctx.respond("Can't wake up users in channels other than the one you're currently in", ephemeral=True)
            return

        await ctx.defer(ephemeral=True)

        for i in range(10):
            await user.move_to(channels[current])
            current = 1 - current

        await ctx.respond(f'Woke up user {user}', ephemeral=True)


def setup(bot):
    bot.add_cog(Basic(bot))
