import os
import glob
import logging
from time import time
import json
import asyncio

import discord
from discord.ext import commands

from dotenv import load_dotenv

# Load dotenv file
load_dotenv("keys.env")
TOKEN = os.getenv("DISCORD")

# Load config file
with open("config.json", "r") as f:
    config = json.load(f)

# Grab vars from config.json
DEFAULT_PREFIX = config["DEFAULT_PREFIX"]
OWNER_IDS = config["OWNER_IDS"]

# Logging
logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{time()}.log",
    filemode="w",
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)

logging.warning("warning")
logging.error("error")
logging.critical("critical")


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX),
            intents=discord.Intents.all(),
            owner_ids=OWNER_IDS,
            #application_id=APP_ID
        )
        self.synced = False
    
    async def sync_tree(self):
        if not self.synced:
            #await tree.sync()
            print("slash commands synced successfully!")
            self.synced = True
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.wait_until_ready()
        print("Bot is now ready!")
        
        await self.sync_tree()
        if not self.ready:
            guild_count = 0
            for guild in self.guilds:
                print(f"- {guild.id} (name: {guild.name})")
                guild_count += 1

            print(f"{self.user} is in {guild_count} guild(s)")

            self.ready = True

MyBot.ready = False
bot = MyBot()
tree = bot.tree

async def load_cogs(bot):
    print("Loading cogs...")
    # loads cogs
    for filename in glob.iglob("./cogs/**", recursive=True):
        if filename.endswith('.py'):
            filename = filename[2:].replace("/", ".") # goes from "./cogs/economy.py" to "cogs.economy.py"
            await bot.load_extension(f'{filename[:-3]}') # removes the ".py" from the end of the filename, to make it into cogs.economy
    

async def main():
    async with bot:
        #await setup(bot)
        await load_cogs(bot)
        await bot.start(TOKEN)

asyncio.run(main())
