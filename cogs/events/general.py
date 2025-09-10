from discord.ext import commands
from mistralai import Mistral
from config import config


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mistral_client = Mistral(api_key=config.mistral_api_key)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user.id in (user.id for user in message.mentions):
            async with message.channel.typing():
                try:
                    response = self.mistral_client.chat.complete(
                        model="mistral-small-latest",
                        messages=[
                            {
                                "role": "user",
                                "content": f"Respond briefly to this message in a friendly, casual way: {message.content}",
                            }
                        ],
                        max_tokens=150,
                    )

                    ai_response = response.choices[0].message.content
                    await message.reply(ai_response)
                except Exception as e:
                    await message.reply(
                        "Sorry, I'm having trouble generating a response right now."
                    )


def setup(bot):
    bot.add_cog(General(bot))
