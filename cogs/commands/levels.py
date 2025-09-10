from mongoengine import connect
from discord.ext import commands
from discord.commands import slash_command, Option
import discord
from config import config
from io import BytesIO
from images.banner_generator import generate_banner
from models.models import Member, Game
import os

connect(host=os.getenv('MONGO_URL'))

NUM_LEADERBOARD_USERS = 10


def loader(amount, max_amount):
    return amount * "⬜" + (max_amount - amount) * "⬛"


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_max_xp(self, lvl):
        return int(round(lvl**config.lvl_curve+config.base_xp, -1))

    def get_all_custom_ranks(self):
        roles = discord.utils.get(
            self.bot.guilds, id=config.guild_ids[0]).roles
        return [discord.utils.get(roles, name=name[0])
                for name in config.rank_names.values()]

    def get_rank_name(self, lvl):
        for key in sorted(config.rank_names.keys(), reverse=True):
            if lvl >= key:
                return config.rank_names[key][0]

    def get_rank_border(self, lvl):
        for key in sorted(config.rank_names.keys(), reverse=True):
            if lvl >= key:
                return config.rank_names[key][1]

    async def show_progress(self, user):
        member = Member.objects.get(uid=user.id)
        max_xp = self.get_max_xp(member.lvl)
        fp = BytesIO()
        await user.avatar.save(fp)
        await generate_banner({'username': user.name, 'level': member.lvl,
                               'progress': member.xp/max_xp, 'border': self.get_rank_border(member.lvl),
                               'avatar': fp})

    async def setup_new_user(self, user):
        if user.bot:
            return
        Member(uid=user.id, xp=0, lvl=0, items=[]).save()
        role = discord.utils.get(discord.utils.get(self.bot.guilds, id=config.guild_ids[0]).roles,
                                 name=config.base_role)
        await user.add_roles(role, reason="Rank System")

    async def remove_previous(self, user, new=None):
        all_custom_ranks = self.get_all_custom_ranks()
        if new is None:
            for role in user.roles:
                if role in all_custom_ranks:
                    await user.remove_roles(role, reason="Rank System")
        else:
            current = set(all_custom_ranks) & set(user.roles)
            current = current.pop() if current else None
            if current != new and current is not None:
                await user.remove_roles(current, reason="Rank System")

    async def set_rank(self, user, new_level):
        roles = discord.utils.get(
            self.bot.guilds, id=config.guild_ids[0]).roles
        await self.remove_previous(user, discord.utils.get(roles, name=self.get_rank_name(new_level)))

        await user.add_roles(discord.utils.get(roles, name=self.get_rank_name(new_level)),
                             reason="Rank System")

    async def add_xp_helper(self, user, amount):
        if not Member.objects(uid=user.id):
            await self.setup_new_user(user)
        member = Member.objects.get(uid=user.id)
        amount += member.xp
        max_xp = self.get_max_xp(member.lvl)

        if not user.bot:
            while amount >= max_xp:
                member.lvl += 1
                amount -= max_xp
                max_xp = self.get_max_xp(member.lvl)
        member.xp = amount
        member.save()
        await self.set_rank(user, member.lvl)

    @slash_command(name='add_xp', description='Add XP to user', guild_ids=config.guild_ids)
    @commands.has_role("Server-Admin")
    async def add_xp(self, ctx: discord.ApplicationContext, user: Option(discord.Member, 'User to add the points to'),
                     amount: Option(int, 'Number of XP points')):
        await self.add_xp_helper(user, amount)
        member = Member.objects.get(uid=user.id)
        await ctx.respond(f'New XP: {member.xp}, New LVL: {member.lvl}', ephemeral=True)

    @slash_command(name='set_roles', description='Role Setup', guild_ids=config.guild_ids)
    @commands.has_role("Server-Admin")
    async def set_roles(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        all_users = list(self.bot.get_all_members())
        embed = discord.Embed()
        embed.add_field(name="Progress ", value=loader(0, len(all_users)), inline=False)

        msg = await ctx.followup.send(embed=embed)

        for users_done, user in enumerate(all_users):
            embed.set_field_at(
                0, name=f'Progress ({users_done} / {len(all_users)}) ', value=loader(users_done, len(all_users)), inline=False)
            await msg.edit(embed=embed)

            if not user.bot:
                await self.remove_previous(user)
                member = Member.objects(uid=user.id)
                if member:
                    member = member[0]
                    role = discord.utils.get(discord.utils.get(self.bot.guilds, id=config.guild_ids[0]).roles,
                                             name=self.get_rank_name(member.lvl))
                    await user.add_roles(role, reason="Rank System")
                else:
                    await self.setup_new_user(user)

        await msg.delete()

        await ctx.followup.send('Role setup done.')

    @slash_command(name='xp', description='Show user progress', guild_ids=config.guild_ids)
    async def xp(self, ctx: discord.ApplicationContext, user: Option(discord.Member, 'User whose progress should be shown')):
        await ctx.defer()

        if user.bot:
            await ctx.followup.send("Cannot show banner of a bot.")
            return

        await self.show_progress(user)
        banner_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'images/banner.png')
        await ctx.followup.send(file=discord.File(banner_path))

    @slash_command(name='time', description="Show user's time spent on server", guild_ids=config.guild_ids)
    async def time(self, ctx: discord.ApplicationContext, user: Option(discord.Member, 'User whose time should be shown')):
        await ctx.defer()

        if user.bot:
            await ctx.followup.send("∞")
            return

        time = 0
        member = Member.objects.get(uid=user.id)
        for i in range(member.lvl):
            time += (self.get_max_xp(i) / 15) * 5
        time += (member.xp / 15) * 5
        await ctx.followup.send(f'{user.mention} has spent {"%.2f" % (time / 60)} hours on Pulsar Server' + (", My pookie 😘" if user.name == "hertarger" else ""));

    @slash_command(name='ranks', description='Show available ranks', guild_ids=config.guild_ids)
    async def ranks(self, ctx: discord.ApplicationContext):
        desc = f'''All the achievable ranks and their levels.
XP needed to progress to next level is generated by this formula: `LEVEL^{config.lvl_curve}+{config.base_xp}`, rounded to the nearest multiple of ten.
You can get XP by spending time in the voice channels. \nRank name and level will be unlocked after the first person reaches it.'''

        embed = discord.Embed(
            title='Ranks', description=desc, color=65535)

        max_level = 0
        for user in self.bot.get_all_members():
            if not user.bot:
                max_level = max(Member.objects.get(uid=user.id).lvl, max_level)

        for level in sorted(config.rank_names.keys()):
            name = config.rank_names[level][0] if level <= max_level else "???????"
            embed.add_field(name=name, value=f'Level: {str(level)}')

        await ctx.respond(embed=embed)

    @slash_command(name='leaderboard', description='Show the leaderboard', guild_ids=config.guild_ids)
    async def leaderboard(self, ctx: discord.ApplicationContext, user: Option(discord.Member, 'User whose progress should be shown') = None, user_count: Option(int, "How many users to show") = 10):
        all_members = [(member.uid, member.lvl) for member in Member.objects]
        all_members = sorted(all_members, key = lambda x: x[1], reverse=True)
        all_members = [(index, member_id, member_lvl) for index, (member_id, member_lvl) in enumerate(all_members)]

        user_index = 0 if user is None else [x[1] for x in all_members].index(user.id)

        start = max(user_index - user_count // 2, 0)
        sliced_members = []

        for x in range(user_count):
            sliced_members.append(all_members[start + x])

        embed = discord.Embed(
            title="Leaderboard", color=7073911)

        for i, member_id, member_lvl in sliced_members:
            member = self.bot.get_user(member_id)

            if (member is None):
                continue

            embed.add_field(
                name=f"{'🔸' if user and user.id == member_id else '🔹'}#{i+1} ~ {member.name}",
                value=f"{member_lvl} - {self.get_rank_name(member_lvl)}", inline=False)

        await ctx.respond(embed=embed)

    @slash_command(name='games', description='Show the game trophies for the user', guild_ids=config.guild_ids)
    async def games(self, ctx: discord.ApplicationContext, user: Option(discord.Member, 'User whose games should be shown')):
        if user.bot:
            await ctx.respond("Can't show game trophies for a bot")
            return

        member = Member.objects.get(uid=user.id)

        embed = discord.Embed(
            title="User Games", color=7073911)

        for game_id in member.games:
            game = Game.objects.get(gid=int(game_id))
            embed.add_field(name=game.name, value=f"{round(game.time/60, 2)}h", inline=False)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Levels(bot))
