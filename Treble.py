import sys
import traceback
import json

import discord
from discord.ext import commands

# Reads json file that has config and retrieves token from the file
with open('config.json', 'r') as configfile:
    configData = configfile.read()
config = json.loads(configData)


# Allows bot to be mentioned or have multiple prefixes to call a command
def get_prefix(bot, message):
    prefixes = [',,']
    if not message.guild:
        return '?'
    return commands.when_mentioned_or(*prefixes)(bot, message)


# List of cogs to be loaded
cogs = [
    'cogs.spotify',
    'cogs.meme'
]

# Loads all the cogs
bot = commands.Bot(command_prefix=get_prefix)
if __name__ == '__main__':
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print('Failed to load cog {}.'.format(cog), file=sys.stderr)
            traceback.print_exc()


# Bot initiation
@bot.event
async def on_ready():
    print('Logged in as {} with ID {}'.format(bot.user.name, bot.user.id))
    await bot.change_presence(activity=discord.Game(' music.'))

bot.run(str(config['token']))
