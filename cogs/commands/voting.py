import discord
from discord.ext import commands
from discord.commands import Option, slash_command
from config import config
from discord.ui import Button, View

def draw_graph(value):
    return value*":white_small_square:" if value > 0 else "▪"


class VoteButton(Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.green)
        self.clicked = set()

    def update_vote(self, embed, add):
        fields = embed.fields
        for index, field in enumerate(fields):
            if field.name.split('|')[0].strip() == self.label:
                break
        name, value = [x.strip() for x in field.name.split('|')]
        value = int(value) + 1 if add else int(value) - 1
        return index, name, value


    async def callback(self, interaction):
        embed = interaction.message.embeds[0]
        uid = interaction.user.id
        if uid not in self.clicked:
            index, name, value = self.update_vote(embed, True)
            embed.set_field_at(
                index, name=f'{name} | {value}', value=draw_graph(value), inline=False)
            self.clicked.add(uid)
            await interaction.response.edit_message(embed=embed)
        else:
            index, name, value = self.update_vote(embed, False)
            embed.set_field_at(
                index, name=f'{name} | {value}', value=draw_graph(value), inline=False)
            self.clicked.remove(uid)
            await interaction.response.edit_message(embed=embed)


class Voting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='vote', description='Vote on a specific topic', guild_ids=config.guild_ids)
    async def vote(self, ctx: discord.ApplicationContext,
                        name: Option(str, 'Enter the name of the vote'),
                        option1: Option(str, 'Enter the vote option'),
                        option2: Option(str, 'Enter the vote option'),
                        option3: Option(str, 'Enter the vote option', required=False, default=None),
                        option4: Option(str, 'Enter the vote option', required=False, default=None),
                        option5: Option(str, 'Enter the vote option', required=False, default=None),
                        option6: Option(str, 'Enter the vote option', required=False, default=None),
                        option7: Option(str, 'Enter the vote option', required=False, default=None),
                        option8: Option(str, 'Enter the vote option', required=False, default=None),
                        option9: Option(str, 'Enter the vote option', required=False, default=None),
                        option10: Option(str, 'Enter the vote option', required=False, default=None),):
        # fucking disgusting, but discord doesn't support variadic arguments in slash commands
        options = [option1, option2, option3, option4, option5, option6,
                    option7, option8, option9, option10]
        options = [x.title() for x in options if x is not None]
        name = name.title()
        embed = discord.Embed(title='------ VOTE: ' +
                                  name+' ------', color=58623)
        view = View(timeout=None)

        for option in options:
            button = VoteButton(label=option)
            view.add_item(button)
            embed.add_field(name=option+" | "+"0",
                                value=draw_graph(0), inline=False)

        await ctx.respond(view=view, embed=embed)


def setup(bot):
    bot.add_cog(Voting(bot))
