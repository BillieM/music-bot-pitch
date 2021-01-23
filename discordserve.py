import discord
from discord.ext import commands
from audioprocess import main
from asyncio import sleep
import os

bot = commands.Bot(command_prefix='#', description='music pitch bot')

pathDir = os.path.abspath(os.path.dirname(__file__))
streamPath = f'{pathDir}/streamAudio'

@bot.event
async def on_ready():
    print('starting...')

@bot.command(name='play')
async def playMusic(ctx, arg1, arg2, arg3):

    fileName, songTitle = main(arg1, arg2, arg3)
    filePath = f'{streamPath}/{fileName}.mp4'

    voiceChannel = ctx.author.voice.channel
    channel = None

    if voiceChannel != None:
        channel = voiceChannel.name
        vc = await voiceChannel.connect()
        await ctx.send(f'playing -> {songTitle}')
        vc.play(discord.FFmpegPCMAudio(source = filePath))
        while vc.is_playing():
            await sleep(.1)
        await ctx.send('song finished!')        
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")

bot.run('ODAyMjI5OTkzODk5Mjk0Nzgx.YAsM5w.OAGfkFGt79Oebxczw8oPt77mEUM')
