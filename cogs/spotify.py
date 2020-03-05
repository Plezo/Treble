import discord
from discord.ext import commands


class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def spotify(self, ctx):
        return

    @spotify.command(name="searchPlaylist", aliases=['sp'])
    async def searchPlaylist(self, ctx, *, arg: str):
        await ctx.send(arg)
        return


def setup(bot):
    bot.add_cog(Spotify(bot))
