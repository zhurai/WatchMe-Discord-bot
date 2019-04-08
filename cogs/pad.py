import os
import sys
from datetime import datetime
import asyncio
import discord
import time
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from bs4 import BeautifulSoup
import requests

scriptdir = os.path.dirname(os.path.abspath('bot.py'))+"\\scripts\\"
padscriptdir = scriptdir+"pad\\"
channelid=int(config.config['BOT']['autochannel'])

class PADCog (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def skyozora_check(self):
        # scrape at reset
        import time
        padtime_scrapeskyozora = '08:01'
        if time.localtime().tm_isdst == 1:
            padtime_scrapeskyozora = '08:01'
        elif time.localtime().tm_isdst == 0:
            padtime_scrapeskyozora = '07:01'
        dailies_time = []
        dailies_string=[]

        while self is self.bot.get_cog("PADCog"):
            now = datetime.strftime(datetime.now(),'%H:%M')
            if now == padtime_scrapeskyozora:
                # scrape current events
                channel = self.bot.get_channel(channelid)
                dst = time.localtime().tm_isdst
                dailies_time=[]
                dailies_string=[]

                r=requests.get("http://pad.skyozora.com/")
                soup = BeautifulSoup(r.content, 'html.parser')
                tables = soup.find("table","sample")
                rows = tables.find_all('tr')

                for i,row in enumerate(rows):
                    if i > 1:
                        cols = row.find_all('td')
                        cols2 = [ele.text.strip() for ele in cols]
                        if i == 2:
                            descends=cols2[1].split(" ")
                            message = "\n".join(descends).rstrip()
                            message = "Today's Descends\n" + message
                            await channel.send("```"+message+"```")
                        elif i == len(rows)-1 or i == len(rows)-2:
                            None
                        else:
                            offset=0
                            if dst==0:
                                offset=16
                            else:
                                offset=15

                            # get the time in UTC+8
                            # cols[0] because I only care about red one
                            time = int(cols2[0][:-1])-offset
                            if time < 0:
                                time=time+24
                            time=str('{0:02d}'.format(time))+":00"
                            dailies_time.append(time)
                            name=row.find_all('td')[0].find('a')["title"]
                            dailies_string.append(name)

                dailies="Today's Guerrilla Schedule\n"
                for i,row in enumerate(dailies_time):
                    dailies = dailies+row+" "+dailies_string[i]+"\n"
                await channel.send("```"+dailies+"```")

                if time.localtime().tm_isdst == 1:
                    padtime_scrapeskyozora = '08:01'
                elif time.localtime().tm_isdst == 0:
                    padtime_scrapeskyozora = '07:01'

                # set timers for it

                await asyncio.sleep(90)
            else:
                await asyncio.sleep(1)


def setup(bot):
    b = PADCog(bot)
    bot.loop.create_task(b.skyozora_check())
    bot.add_cog(b)
