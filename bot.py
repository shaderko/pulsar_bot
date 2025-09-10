import discord
from config import config
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

bot = discord.Bot(intents=config.intents)

for extension in config.startup_extensions:
    try:
        bot.load_extension(extension)
        logging.info(f"Loaded extension: {extension}")
    except Exception as e:
        logging.info(f"Failed to load extension {extension}, with err: {e}")

bot.run(config.token)

