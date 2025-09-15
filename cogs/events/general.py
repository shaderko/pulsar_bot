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
                    # Fetch last 5 messages for context
                    messages_history = []
                    async for msg in message.channel.history(limit=6, before=message):
                        if not msg.author.bot:  # Skip bot messages in context
                            messages_history.append(
                                f"{msg.author.display_name}: {msg.content}")

                    # Reverse to get chronological order and take last 5
                    messages_history.reverse()
                    context_messages = messages_history[-5:] if len(
                        messages_history) > 5 else messages_history

                    # Build context string
                    context = "\n".join(
                        context_messages) if context_messages else "No recent context available."

                    response = self.mistral_client.chat.complete(
                        model="mistral-small-latest",
                        messages=[
                            {
                                "role": "user",
                                "content": f"Here's the recent conversation context:\n{context}\n\nNow respond briefly to this message: {message.content}",
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
