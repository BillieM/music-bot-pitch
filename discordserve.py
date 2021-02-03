import discord
from discord.ext import commands
from audioprocess import main
from asyncio import sleep
import os

bot = commands.Bot(command_prefix='#', description='music pitch bot')
apiToken = os.environ.get('MUSIC-BOT')
pathDir = os.path.abspath(os.path.dirname(__file__))
streamPath = f'{pathDir}/streamAudio'

queueDict = {}

def getQueueObject(serverId):
    if serverId in queueDict:
        return queueDict[serverId]
    else:
        queue = Queue()
        queueDict[serverId] = queue
        return queue

def getSongString(songDict):
    songTitle = songDict['name']
    try:
        speed = float(songDict['speed'])
    except:
        speed = 1
    try:
        reverb = float(songDict['reverb'])
    except:
        reverb = 0
    try:
        overdrive = float(songDict['overdrive'])
    except: 
        overdrive = 0

    songString = f'{songTitle} [{speed}x speed, {reverb}% reverb, {overdrive}db overdrive]'
    return songString

class Queue():
    def __init__(self):
        self.queueList = []
        self.playing = False
        self.vc = None
        self.skip = False

    def addToQueue(self, fileName, filePath, speed, reverb, overdrive):
        self.queueList.append({'name': fileName, 'path': filePath, 'speed': speed, 'reverb': reverb, 'overdrive': overdrive})
        return self.queueList[-1]

    def removeCurrentSong(self):
        self.queueList.pop(0)

    def getNextSong(self):
        nextSong = self.queueList[0]

        return nextSong

    def isNextSong(self):
        if len(self.queueList) > 0:
            return True
        else:
            return False

    def getQueueString(self):
        if len(self.queueList) > 0:
            queueItems = []
            for i, song in enumerate(self.queueList):
                songString = getSongString(song)
                if i == 0:
                    i = "currently playing"
                queueItems.append(f'{i} - {songString}')
            queueString = '\n💕💕💕 the queue 💕💕💕\n' + ''.join([f'\n{queueItem}\n' for queueItem in queueItems]) + '\n\n'
            return queueString
        else:
            return "queue is empty! use #play to add to queue"

queue = Queue()

@bot.event
async def on_ready():
    print('starting...')

@bot.command(name = 'skip')
async def skipSong(ctx):
    queue = getQueueObject(ctx.guild.id)
    queue.skip = True

@bot.command(name = 'remove')
async def removeSong(ctx, arg1):
    queue = getQueueObject(ctx)
    try:
        song = queue.queueList[arg1]
        songString = getSongString(song)
        await ctx.send(f'removing song {songString}')
        queue.queueList.remove(song)
    except Exception as e:
        await ctx.send(e)

@bot.command(name = 'queue')
async def showQueue(ctx):
    queue = getQueueObject(ctx.guild.id)
    await ctx.send(queue.getQueueString())

@bot.command(name='play')
async def queueMusic(ctx, arg1, arg2=None, arg3=None, arg4=None):

    queue = getQueueObject(ctx.guild.id)

    voiceChannel = ctx.author.voice.channel

    if voiceChannel != None:
        try:
            fileName, songTitle = await main(arg1, arg2 , arg3, arg4)
            filePath = f'{streamPath}/{fileName}.mp4'
            queuedSong = queue.addToQueue(songTitle, filePath, speed = arg2, reverb = arg3, overdrive = arg4)
            queuedSongString = getSongString(queuedSong)
            if not queue.playing:
                await playMusic(ctx)
            else:
                await ctx.send(f'queued -> {queuedSongString}') 

        except Exception as e:
            await ctx.send(e)
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")

async def playMusic(ctx):

    queue = getQueueObject(ctx.guild.id)

    voiceChannel = ctx.author.voice.channel

    if not queue.playing:
        queue.playing = True
        queue.vc = await voiceChannel.connect()

    nextSong = queue.getNextSong()

    nextSongPath = nextSong['path']
    nextSongString = getSongString(nextSong)

    await ctx.send(f"now playing - {nextSongString}")
    queue.vc.play(discord.FFmpegPCMAudio(source = nextSongPath))

    while queue.vc.is_playing():
        if not queue.skip:
            await sleep(0.1)
        else:
            queue.vc.stop()
            queue.skip = False
    else:
        await ctx.send("song finished/ skipped!")
    
    queue.removeCurrentSong()

    if queue.isNextSong():
        await playMusic(ctx)
    else:
        await ctx.send("queue finished, disconnecting")
        queue.playing = False
        await queue.vc.disconnect()
        
bot.run(apiToken)