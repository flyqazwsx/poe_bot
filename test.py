import asyncio
import discord
from discord.ext import commands
import json
import random

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

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


def get_chrome(url, driver=r'C:\Users\admin\Desktop\程式\python\chromedriver.exe', wait=10, hide=True):
    try:
        # 隱藏瀏覽器
        options = webdriver.ChromeOptions()
        if hide:
            options.add_argument('--headless')

        service = Service(driver)
        chrome = webdriver.Chrome(service=service, options=options)
        chrome.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        chrome.get(url)
        cookie = {'name': 'POESESSID',
                  'value': 'af335e18860130a820444f8ff5f73d5c'}
        chrome.add_cookie(cookie_dict=cookie)

        chrome.implicitly_wait(wait)
        chrome.get(url)

        return chrome
    except Exception as e:
        print(e)


@bot.command()
async def c價(ctx):
    url = 'https://web.poe.garena.tw/trade/exchange/%E5%8D%A1%E8%98%AD%E5%BE%B7'
    chrome = get_chrome(url)
    time.sleep(3)
    xpath = '/html/body/div[2]/div/div[1]/div[4]/div[3]/ul[1]/li[2]/a'
    element = chrome.find_element(by=By.XPATH, value=xpath)
    element.click()
    time.sleep(3)
    xpath = '/html/body/div[2]/div/div[1]/div[4]/div[4]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[2]/div[4]'
    element = chrome.find_element(by=By.XPATH, value=xpath)
    element.click()
    time.sleep(3)
    xpath = '/html/body/div[2]/div/div[1]/div[4]/div[4]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div[17]'
    element = chrome.find_element(by=By.XPATH, value=xpath)
    element.click()
    time.sleep(3)
    xpath = '/html/body/div[2]/div/div[1]/div[4]/div[4]/div/div[3]/div[2]/button'
    element = chrome.find_element(by=By.XPATH, value=xpath)
    element.click()
    time.sleep(3)
    chrome.page_source
    soup_url = BeautifulSoup(chrome.page_source, 'lxml')

    time.sleep(3)
    exs = soup_url.find('div', class_="resultset exchange").find_all(
        'span', class_="amount")

    zx = [div.text.strip() for div in exs]
    x = np.array(zx).reshape((-1, 2))
    df = pd.DataFrame(x)
    df[1] = df[1].astype(float)
    df = df[df[1] >= 1]
    df1 = df.head().max()

    await ctx.send(f'目前最高價')
    await ctx.send(df1)

    await ctx.send(f'平均價格')
    df = df.value_counts()
    await ctx.send(df.head(10))
    chrome.quit()


# @bot.command()
# async def 物價(ctx):
#     try:
#         Search = str(echo(ctx))
#         url = 'https://web.poe.garena.tw/trade/search/%E5%8D%A1%E8%98%AD%E5%BE%B7'
#         chrome = get_chrome(url)

#         time.sleep(3)
#         xpath = '/html/body/div[2]/div/div[1]/div[4]/div[4]/div/div[1]/div[1]/div/div[2]/input'
#         element = chrome.find_element(by=By.XPATH, value=xpath)
#         element.click()
#         time.sleep(3)

#         element.send_keys(Search)
#         time.sleep(3)

#         element.send_keys('\ue007')

#         time.sleep(3)
#         xpath = '/html/body/div[2]/div/div[1]/div[4]/div[4]/div/div[3]/div[2]/button'
#         element = chrome.find_element(by=By.XPATH, value=xpath)
#         element.click()
#         time.sleep(3)
#         chrome.page_source
#         soup_url = BeautifulSoup(chrome.page_source, 'lxml')
#         time.sleep(3)
#         soup_url.find('div', class_="results").find_all('span')
#         time.sleep(3)

#         x = soup_url.find_all('span', class_="s sorted sorted-asc")

#         for c in x:
#             await ctx.send(c.text.strip())

#         chrome.quit()
#     except Exception as e:
#         print(e)


# @bot.event
# async def on_message(message):
#     if message.content.startswith('$greet'):
#         channel = message.channel
#         await channel.send('Say hello!')

#         def check(m):
#             return m.content == 'hello' and m.channel == channel

#         msg = await bot.wait_for('message', check=check)
#         await channel.send(f'Hello {msg.author}!')


@bot.command(
    name="echo",
    description="A simple command that repeats the usert imput back to them. ",
)
async def echo(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Please tell me what you want me to repeat",
        description="1 minute"
    )
    sent = await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=60,
            check=lambda message: message.author == ctx.author
            and message.channel == ctx.channel
        )
        if msg:
            await sent.delete()
            await msg.delete()
            await ctx.send(msg.content)
            return msg.content
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send("Cancelling due to timeout.", delete_after=10)


@bot.command(name="物價",
             description="A simple command that repeats the usert imput back to them. ",)
async def 物價(ctx):

    await ctx.message.delete()
    embed = discord.Embed(
        title="Please tell me what you want me to repeat",
        description="1 minute"
    )
    sent = await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for(
            "message",
            timeout=60,
            check=lambda message: message.author == ctx.author
            and message.channel == ctx.channel
        )
        if msg:
            await sent.delete()
            await msg.delete()
            await ctx.send(msg.content)
            set_msg = msg.content
    except asyncio.TimeoutError:
        await sent.delete()
        await ctx.send("Cancelling due to timeout.", delete_after=10)

    try:
        Search = str(set_msg)
        url = 'https://web.poe.garena.tw/trade/search/%E5%8D%A1%E8%98%AD%E5%BE%B7'
        chrome = get_chrome(url)

        time.sleep(3)
        xpath = '/html/body/div[2]/div/div[1]/div[4]/div[4]/div/div[1]/div[1]/div/div[2]/input'
        element = chrome.find_element(by=By.XPATH, value=xpath)
        element.click()
        time.sleep(3)

        element.send_keys(Search)
        time.sleep(3)

        element.send_keys('\ue007')

        time.sleep(3)
        xpath = '/html/body/div[2]/div/div[1]/div[4]/div[4]/div/div[3]/div[2]/button'
        element = chrome.find_element(by=By.XPATH, value=xpath)
        element.click()
        time.sleep(3)
        chrome.page_source
        soup_url = BeautifulSoup(chrome.page_source, 'lxml')
        time.sleep(3)
        soup_url.find('div', class_="results").find_all('span')
        time.sleep(3)

        x = soup_url.find_all('span', class_="s sorted sorted-asc")

        for c in x:
            await ctx.send(c.text.strip())

        chrome.quit()
    except Exception as e:
        print(e)


bot.run(data['TOKEN'])
