from discord.ext import commands
from discord.commands import permissions, slash_command


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='ld', hidden=True)
    @permissions.has_role("Server-Admin")
    async def load(self, ctx, module: str):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @slash_command(name='ud', hidden=True)
    @permissions.has_role("Server-Admin")
    async def unload(self, ctx, module: str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @slash_command(name='rd', hidden=True)
    @permissions.has_role("Server-Admin")
    async def reload(self, ctx, module: str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')


def setup(bot):
    bot.add_cog(Admin(bot))
