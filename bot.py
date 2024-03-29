import config
import utils
import requests
import subprocess
import os
import sys
import discord
import pyautogui
from discord.ext import commands

localconfig = config.config['BOT']
scriptdir = os.path.dirname(os.path.abspath(__file__))+"\\scripts\\"
token = config.config['BOT']['discordtoken']
prefix= config.config['BOT']['prefix']

# create Discord Client
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print("Logged in")
    print("Username: " + bot.user.name)
    print("ID: " + str(bot.user.id))
    print("-----")
    if localconfig.getint('hide') == 1:
        proc = subprocess.Popen(['C:\Program Files (x86)\AutoIt3\AutoIt3.exe',scriptdir+'startup_bot.hide.au3'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    else:
        proc = subprocess.Popen(['C:\Program Files (x86)\AutoIt3\AutoIt3.exe',scriptdir+'startup_bot.show.au3'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

bot.load_extension("cogs.management")
bot.load_extension("cogs.watchme")
bot.load_extension("cogs.pad")

'''
# Test commands to set the stage for later

@bot.command()
async def test_bat(ctx):
    print(scriptdir+'\test.bat')
    proc = subprocess.Popen([scriptdir+'test.bat'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout_value = proc.stdout.read() + proc.stderr.read()
    await ctx.send(stdout_value)

@bot.command()
async def test_autoit(ctx):
    proc = subprocess.Popen(['C:\Program Files (x86)\AutoIt3\AutoIt3.exe','test.au3'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout_value = proc.stdout.read() + proc.stderr.read()
    return

@bot.command()
async def test_python(ctx):
    # python.exe based ones on PATH don't need full path
    proc = subprocess.Popen(['python.exe','test.py'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout_value = proc.stdout.read() + proc.stderr.read()
    await ctx.send(stdout_value)

# this is actually unsafe to have

@bot.command()
async def cmd(ctx,*args):
    print("cmd - ", args)
    proc = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    stdout_value = proc.stdout.read() + proc.stderr.read()
    await ctx.send(stdout_value.rstrip().decode())
'''


# start bot
bot.run(token)
