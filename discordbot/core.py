import discord
from discord.ext import commands
from asyncio import sleep
import os
import traceback
from queues import Queues
from songs import Song

bot = commands.Bot(command_prefix='#', description='music pitch bot')
apiToken = os.environ.get('MUSICBOT')
dirs = Dirs()
queues = Queues(dirs)

async def addToQueue(ctx, arg1, arg2, arg3, arg4, reverse):

    queue = queues.getQueueObject(ctx.guild.id)

    voiceChannel = ctx.author.voice.channel

    if voiceChannel != None:
        try:
            song = Song(
                searchTerm = arg1
            )
            song.processSong()
            queue.addToQueue(song)
            if not queue.playing:
                await playMusic(ctx)
            else:
                await ctx.send(f'queued -> {song}')
        except Exception as e:
            ctx.send(e)
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")

@bot.event
async def on_ready():
    print('starting...')

@bot.command(name = 'skip')
async def skipSong(ctx):
    queue = queues.getQueueObject(ctx.guild.id)
    queue.skip = True

@bot.command(name = 'remove')
async def removeSong(ctx, arg1):
    queue = queue.getQueueObject(ctx.guild.id)
    try:
        song = queue.queueList[int(arg1)]
        songString = getSongString(song)
        await ctx.send(f'removing song {songString}')
        queue.queueList.remove(song)
    except Exception as e:
        await ctx.send(e)
        print(traceback.format_exc())

@bot.command(name = 'queue')
async def showQueue(ctx):
    queue = queues.getQueueObject(ctx.guild.id)
    await ctx.send(queue)

@bot.command(name='play')
async def queueMusic(ctx, arg1, arg2=None, arg3=None, arg4=None):
    await addToQueue(ctx, arg1, arg2, arg3, arg4, reverse=False)

@bot.command(name='revplay')
async def queueRevMusic(ctx, arg1, arg2=None, arg3=None, arg4=None):
    await addToQueue(ctx, arg1, arg2, arg3, arg4, reverse=True)


async def playMusic(ctx):

    queue = queues.getQueueObject(ctx.guild.id)

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