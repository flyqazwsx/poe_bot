import discord
from discord.ext import commands
import json
import random

with open('setting.json', 'r', encoding='utf8') as file:
    data = json.load(file)

intents = discord.Intents.all()
# intents = discord.Intents.default()
# intents.members = True


bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(">> Bot is online <<")


# 成員加入事件
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(data['Welcome_channel']))
    await channel.send(f'{member} join!')


# 成員離開事件
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(data['Leave_channel']))
    await channel.send(f'{member} leave!')


# ctx=context(上下文) ctx包含參數(使用使,id,所在伺服器,所在頻道)
@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} (ms)')


@bot.command()
async def 圖片(ctx):
    random_image = random.choice(data['image'])
    image = discord.File(random_image)
    await ctx.send(file=image)


bot.run(data['TOKEN'])
