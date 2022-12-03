import asyncio
import os
import discord

from discord.ext import commands
import json
import random
import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from core.classes import Cog_Extension


def get_chrome(url, driver=r'D:\程式\python\chromedriver.exe', wait=10, hide=True):
    # driver=r'C:\Users\admin\Desktop\程式\python\chromedriver.exe'
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


class poe(Cog_Extension):

    @commands.command()
    async def c價(self, ctx):
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

    # @commands.command(
    #     name="echo",
    #     description="A simple command that repeats the usert imput back to them. ",
    # )
    # async def echo(self,ctx):
    #     await ctx.message.delete()
    #     # 嵌入訊息
    #     embed = discord.Embed(
    #         title="Please tell me what you want me to repeat",
    #         color=0x1fd5d5
    #     )
    #     sent = await ctx.send(embed=embed)

    #     try:
    #         # 使用者輸入
    #         msg = await commands.wait_for(
    #             "message",
    #             timeout=60,
    #             check=lambda message: message.author == ctx.author
    #             and message.channel == ctx.channel
    #         )
    #         if msg:
    #             await sent.delete()
    #             await msg.delete()
    #             await ctx.send(msg.content)
    #             return msg.content
    #     except asyncio.TimeoutError:
    #         await sent.delete()
    #         await ctx.send("Cancelling due to timeout.", delete_after=10)


async def setup(bot):
    await bot.add_cog(poe(bot))
