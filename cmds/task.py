import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import asyncio
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


class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = 0

        # 每隔5秒啟動
        # async def inerval():
        #     await self.bot.wait_until_ready()
        #     self.channel = self.bot.get_channel(1048598702312403015)
        #     while not self.bot.is_closed():
        #         await self.channel.send("Hi Im running!")
        #         await asyncio.sleep(5)

        # self.bg_task = self.bot.loop.create_task(inerval())

        # 手動輸入特定時間啟動

        async def time_task():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(1048598702312403015)
            while not self.bot.is_closed():
                now_time = datetime.datetime.now().strftime('%H%M')
                with open('setting.json', 'r', encoding='utf8') as file:
                    data = json.load(file)
                if now_time == data['time'] and self.counter == 0:
                    await self.channel.send('Task Working!')
                    self.counter = 1
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(1)
                    pass

        self.bg_task = self.bot.loop.create_task(time_task())

        async def poe_time():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(1048598702312403015)
            while not self.bot.is_closed():
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
                await self.channel.send(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                await self.channel.send(f'目前最高價')
                await self.channel.send(df1)

                await self.channel.send(f'平均價格')
                df = df.value_counts()
                await self.channel.send(df.head(10))
                chrome.quit()
                await asyncio.sleep(300)

        self.bg_task = self.bot.loop.create_task(poe_time())

    # 在Discord手動更換頻道
    @ commands.command()
    async def set_channel(self, ctx, ch: int):
        self.channel = self.bot.get_channel(ch)
        await ctx.send(f'Set Channel:{self.channel.mention}')

    # 手動輸入特定時間啟動

    @ commands.command()
    async def set_time(self, ctx, time):
        self.counter = 0
        with open('setting.json', 'r', encoding='utf8') as file:
            data = json.load(file)
        data['time'] = time
        with open('setting.json', 'w', encoding='utf8') as file:
            json.dump(data, file, indent=4)


async def setup(bot):
    await bot.add_cog(Task(bot))
