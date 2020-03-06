import urllib3
import requests
import json

import discord
from discord.ext import commands

http = urllib3.PoolManager()

# Parses config json for imgflip username and password
with open('config.json', 'r') as configfile:
    configData = configfile.read()
config = json.loads(configData)
imgflip = config['imgflip']


# Used to retrieve imgflips id for the meme specified
def getMemeID(name):
    imgflipMemes = requests.get('https://api.imgflip.com/get_memes')

    for i in range(len(imgflipMemes.json()['data']['memes'])):
        jsonData = imgflipMemes.json()['data']['memes'][i]

        if jsonData['name'] in name:
            return jsonData['id']
    return 0


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Groups these commands to be under the name meme
    @commands.group()
    async def meme(self, ctx):
        return

    # Sends all meme templates with their corresponding urls
    @meme.command(name="getMemes", aliases=['gm', 'getlist'])
    async def getMemes(self, ctx):
        imgflipMemes = requests.get('https://api.imgflip.com/get_memes')
        embedNames = discord.Embed(title='Meme templates',
                                   colour=discord.Color.dark_teal())

        for i in range(len(imgflipMemes.json()['data']['memes'])):
            jsonData = imgflipMemes.json()['data']['memes'][i]
            embedNames.add_field(name=jsonData['name'], value=jsonData['url'])
            if len(embedNames.fields) >= 24:
                await ctx.send(embed=embedNames)
                embedNames.clear_fields()

    # Sends a meme with the provided captions and specified template
    @meme.command(name="createMeme", aliases=['create', 'c'])
    async def createMeme(self, ctx, *, arg: str):
        arglist = arg.split('|')
        meme = arglist[0]
        memeID = getMemeID(meme)
        arglist = arglist[1:]
        data = (('username', imgflip['username']), ('password', imgflip['password']), ('template_id', memeID))
        if memeID == 0:
            await ctx.send(embed=discord.Embed(
                title="Invalid template",
                color=discord.Color.dark_red()
            ))
            return

        for i in range(len(arglist)):
            data = data + (('text{}'.format(i), arglist[i]),)
        res = requests.post(url='https://api.imgflip.com/caption_image', data=data)

        await ctx.message.delete()
        await ctx.send(embed=discord.Embed().set_image(url=res.json()['data']['url']))


def setup(bot):
    bot.add_cog(Meme(bot))
