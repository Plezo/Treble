from urllib.request import urlopen
import json

import discord
from discord.ext import commands

# Reads json file that has config and retrieves token from the file
with open('config.json', 'r') as configfile:
    configData = configfile.read()
config = json.loads(configData)
clientid = str(config['spotifyID'])


class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def spotify(self, ctx):
        login = urlopen("https://accounts.spotify.com/authorize?response_type=code&client_id={}&redirect_uri=".format(clientid))
        return

    @spotify.command(name="searchPlaylist", aliases=['sp'])
    async def searchPlaylist(self, ctx, *, arg: str):
        spotify = urlopen("https://api.spotify.com/v1/search?q={}&type=playlist&limit=5".format(arg.replace(' ', '+')))
        print(spotify.read())


def setup(bot):
    bot.add_cog(Spotify(bot))
