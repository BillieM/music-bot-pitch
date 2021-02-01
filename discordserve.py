import discord
from discord.ext import commands
from audioprocess import main
from asyncio import sleep
import os

bot = commands.Bot(command_prefix='#', description='music pitch bot')

pathDir = os.path.abspath(os.path.dirname(__file__))
streamPath = f'{pathDir}/streamAudio'

class Queue():
    def __init__(self):
        self.queueList = []
        self.playing = False
        self.vc = None
        self.skip = False

    def addToQueue(self, fileName, filePath):
        self.queueList.append({'name': fileName, 'path': filePath})

    def removeCurrentSong(self):
        self.queueList.pop(0)

    def getNextSong(self):
        nextSongTitle = self.queueList[0]['name']
        nextSongPath = self.queueList[0]['path']

        return nextSongTitle, nextSongPath

    def isNextSong(self):
        if len(self.queueList) > 0:
            return True
        else:
            return False
        
queue = Queue()

@bot.event
async def on_ready():
    print('starting...')

@bot.command(name = 'skip')
async def skipSong(ctx):
    queue.skip = True

@bot.command(name='play')
async def queueMusic(ctx, arg1, arg2=None, arg3=None, arg4=None):

    voiceChannel = ctx.author.voice.channel

    if voiceChannel != None:
        fileName, songTitle = await main(arg1, arg2 , arg3, arg4)
        filePath = f'{streamPath}/{fileName}.mp4'
        queue.addToQueue(songTitle, filePath)
        await ctx.send(f'queued -> {songTitle}') 
        if not queue.playing:
            print("queue not playing")
            await playMusic(ctx)
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")

async def playMusic(ctx):

    voiceChannel = ctx.author.voice.channel

    if not queue.playing:
        queue.vc = await voiceChannel.connect()

    nextSongTitle, nextSongPath = queue.getNextSong()

    queue.vc.play(discord.FFmpegPCMAudio(source = nextSongPath))

    while queue.vc.is_playing():
        if not queue.skip:
            await sleep(0.1)
        else:
            queue.vc.stop()
            queue.skip = False

    queue.removeCurrentSong()

    if queue.isNextSong():
        await playMusic(ctx)
    else:
        await queue.vc.disconnect()
        
bot.run('ODAyMjI5OTkzODk5Mjk0Nzgx.YAsM5w.OAGfkFGt79Oebxczw8oPt77mEUM')


'''
@bot.command(name='play')
async def queueMusic(ctx, arg1, arg2=None, arg3=None, arg4=None):

    voiceChannel = ctx.author.voice.channel
    channel = None

    if voiceChannel != None:

        fileName, songTitle = main(arg1, arg2 , arg3, arg4)
        filePath = f'{streamPath}/{fileName}.mp4'

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



'''