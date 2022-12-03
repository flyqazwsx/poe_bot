import discord
from discord.ext import commands
import random
import json
from core.classes import Cog_Extension

with open('setting.json', 'r', encoding='utf8') as file:
    data = json.load(file)


class React(Cog_Extension):

    @commands.command()
    async def 圖片(self, ctx):
        random_image = random.choice(data['image1'])
        image = discord.File(random_image)
        await ctx.send(file=image)


async def setup(bot):
    await bot.add_cog(React(bot))
