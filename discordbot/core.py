import discord
from discord.ext import commands
from asyncio import sleep
import os
import traceback
from queues import Queues
from songs import Song
from dirs import Dirs
from random import choice

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix='#',
    description='music pitch bot',
    intents=intents
)
apiToken = os.environ.get('MUSICBOT')
dirs = Dirs()
dirs.dirsSetup()
queues = Queues(dirs)

# force send messages to specific channel on these servers
forceChannelServers = {
    595971332991090717: 1069981278948044890
}


async def addToQueue(ctx, arg1, arg2, arg3, arg4, reverse):

    queue = queues.getQueueObject(ctx.guild.id)

    voiceChannel = ctx.author.voice.channel

    if voiceChannel != None:
        try:
            song = Song(
                dirs=dirs,
                searchTerm=arg1,
                reverse=reverse,
                speed=arg2,
                reverb=arg3,
                overdrive=arg4
            )

            await song.processSong()

            queue.addToQueue(song)
            if not queue.playing:
                await playMusic(ctx)
            else:
                await sendMessage(ctx, f'queued -> {song}')
        except Exception as e:
            await sendMessage(ctx, traceback.format_exc())
            print(traceback.format_exc())
    else:
        await sendMessage(ctx, str(ctx.author.name) + "is not in a channel.")


@bot.event
async def on_ready():
    print('starting...')


@bot.command(name='skip')
async def skipSong(ctx):
    queue = queues.getQueueObject(ctx.guild.id)
    queue.skip = True


@bot.command(name='remove')
async def removeSong(ctx, arg1):
    queue = queues.getQueueObject(ctx.guild.id)
    try:
        song = queue[int(arg1)]
        await sendMessage(ctx, f'removing song {song}')
        queue.queueList.remove(song)
    except Exception as e:
        await sendMessage(ctx, e)
        print(traceback.format_exc())


@bot.command(name='queue')
async def showQueue(ctx):
    queue = queues.getQueueObjectsend(ctx.guild.id)
    await sendMessage(ctx, queue)


@bot.command(name='play')
async def queueMusic(ctx, arg1, arg2=None, arg3=None, arg4=None):
    await addToQueue(ctx, arg1, arg2, arg3, arg4, reverse=False)


@bot.command(name='revplay')
async def queueRevMusic(ctx, arg1, arg2=None, arg3=None, arg4=None):
    await addToQueue(ctx, arg1, arg2, arg3, arg4, reverse=True)


@bot.command(name='roulette')
async def roulette(ctx):
    members = ctx.message.guild.members

    while True:
        selected = choice(members)
        if not selected.bot:
            break
    
    msg = f'{selected.display_name} ({selected}) HAS BEEN SELECTED.'

    await sendMessage(ctx, msg)

async def playMusic(ctx):

    queue = queues.getQueueObject(ctx.guild.id)

    voiceChannel = ctx.author.voice.channel

    if not queue.playing:
        queue.playing = True
        queue.vc = await voiceChannel.connect()

    song = queue.getNextSong()

    await sendMessage(ctx, f"now playing:\n{song}")
    queue.vc.play(discord.FFmpegPCMAudio(source=song.streamPath))

    while queue.vc.is_playing():
        if not queue.skip:
            await sleep(0.1)
        else:
            queue.vc.stop()
            queue.skip = False
    else:
        await song.postStreamClean()
        await sendMessage(ctx, "song finished/ skipped!")

    queue.removeCurrentSong()

    if queue.isNextSong():
        await playMusic(ctx)
    else:
        await sendMessage(ctx, "queue finished, disconnecting")
        queue.playing = False
        await queue.vc.disconnect()


async def sendMessage(ctx, msg):

    if ctx.guild.id in forceChannelServers:
        channel = bot.get_channel(forceChannelServers[ctx.guild.id])
        await channel.send(msg)
    else:
        await ctx.send(msg)

bot.run(apiToken)
