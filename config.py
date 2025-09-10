import discord
import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

        self.intents = discord.Intents.default()
        self.intents.members = True
        self.intents.reactions = True
        self.intents.voice_states = True
        self.intents.presences = True
        self.token = os.getenv('DISCORD_TOKEN')
        self.mistral_api_key = os.getenv('MISTRAL_API_KEY')
        self.activity = discord.Game(name="5D Chess")
        self.startup_extensions = ["cogs.events.bot_startup",
                                   "cogs.commands.basic",
                                   "cogs.commands.voting",
                                   "cogs.commands.levels",
                                   "cogs.events.activity",
                                   "cogs.commands.split",
                                   "cogs.events.split_cleanup",
                                   "cogs.events.general",
                                   "cogs.commands.remind",
                                   "cogs.events.birthday",
                                   "cogs.commands.birthday",]
        self.afk_channel = 487675283617480704
        self.birthday_channel = 287295223649009665
        self.guild_ids = [287295223649009665]
        self.split_prefix = "PULSAR_SPLIT"
        self.base_role = 'Initiate'
        self.lvl_curve = 1.4
        self.base_xp = 200
        self.active_xp = 15
        self.rank_names = {
            0: ('Initiate', 1),
            10: ('Apprentice', 2),
            20: ('Scholar', 3),
            30: ('Mentor', 4),
            40: ('Expert', 5),
            50: ('Chief', 6),
            60: ('Heroic', 7),
            70: ('Lord', 8),
            80: ('Demonlord', 9),
            90: ('Sentinel', 10),
            100: ('Inquisitor', 11),
            110: ('Conqueror', 12),
            120: ('Vanquisher', 13),
            130: ('Master', 14),
            140: ('Warmaster', 15),
            150: ('Champion', 16),
            160: ('Legend', 17),
            170: ('Demigod', 18),
            180: ('Immortal', 19),
            190: ('Emperor', 20),
            200: ('Overlord', 21)}
        self.banner = 'images/borders/backdrop-magic.png'


config = Config()
