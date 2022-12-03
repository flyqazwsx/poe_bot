import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json', 'r', encoding='utf8') as file:
    data = json.load(file)


class Main(Cog_Extension):

    # ctx=context(上下文) ctx包含參數(使用使,id,所在伺服器,所在頻道)
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

    # 成員加入事件
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(data['Welcome_channel']))
        await channel.send(f'{member} join!')

    # 成員離開事件
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(int(data['Leave_channel']))
        await channel.send(f'{member} leave!')

    # 關鍵字觸發
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == 'apple' and msg.author != self.bot.user:
            await msg.channel.send('蘋果')


async def setup(bot):
    await bot.add_cog(Main(bot))
