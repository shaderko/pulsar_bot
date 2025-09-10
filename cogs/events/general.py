from discord.ext import commands
import markovify


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.id in (user.id for user in message.mentions):
            async with message.channel.typing():
                with open('markov/model.json', 'r') as file:
                    file = file.read()
                    model = markovify.NewlineText.from_json(file)

                    sentence = model.make_sentence()

                    await message.reply(sentence)


def setup(bot):
    bot.add_cog(General(bot))