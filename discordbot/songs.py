import os
import shutil
import random
import traceback

from youtubesearchpython import VideosSearch
from pytube import YouTube
from pydub import AudioSegment
from pysndfx import AudioEffectsChain

class Song():

    '''
    Class used for downloading songs/ processing audio

    would like to implement multithreading here
    '''
    def __init__(self, dirs, searchTerm, reverse = False, speed = 1, reverb = 0, overdrive = 0):
        self.dirs = dirs
        self.searchTerm = searchTerm
        self.reverse = reverse
        self.speed = speed
        self.reverb = reverb
        self.overdrive = overdrive
        self.videoSearch = None
        self.title = None
        self.duration = None
        self.url = None
        self.fileName = None
        self.streamPath = None

    def __repr__(self):
        
        modString = ''
        titleString = self.title

        if self.speed != None:
            modString += f'{self.speed}x speed, '

        if self.reverb != None:
            modString += f'{self.reverb}% reverb, '
            
        if self.overdrive != None:
            modString += f'{self.speed}db overdrive, '

        modString = modString.rstrip(', ')

        if self.reverse:
            titleString = titleString[::-1]

        songString = titleString

        if len(modString) > 0:
            songString = f'{songString} [{modString}]'

        return songString

    async def processSong(self):
        await self.getVideoSearchObject()
        await self.extractInfoFromVideoSearch()
        await self.downloadFromYoutube()
        await self.mp4ToWav()
        await self.addAudioEffects()
        await self.wavToMp4()
        await self.preStreamClean()

    async def getVideoSearchObject(self):
        '''
        retry 3x
        '''
        for i in range(3):
            try:
                videoSearch = VideosSearch(self.searchTerm, limit = 3).result()
                self.videoSearch = videoSearch['result'][i]
                break
            except Exception as e:
                print(traceback.format_exc())
        
    async def extractInfoFromVideoSearch(self):
        self.title = self.videoSearch['title']
        self.duration = self.videoSearch['duration']  
        self.url = self.videoSearch['link']
        self.fileName = self.videoSearch['id']

    async def downloadFromYoutube(self):
        downloadedAudioDirPath = self.dirs['downloadedAudio'].dirPath
        songPath = f'{downloadedAudioDirPath}/{self.fileName}.mp4'

        if not os.path.isfile(songPath):
            yt = YouTube(self.url)
            audioStream = yt.streams.filter(only_audio=True).first()
            audioStream.download(downloadedAudioDirPath, filename=self.fileName)

    async def mp4ToWav(self):
        mp4DirPath = self.dirs['downloadedAudio'].dirPath
        wavDirPath = self.dirs['wavAudio'].dirPath
        mp4Path = f'{mp4DirPath}/{self.fileName}.mp4'
        wavPath = f'{wavDirPath}/{self.fileName}.wav'
        audio = AudioSegment.from_file(mp4Path)
        audio.export(wavPath, format = 'wav')

    async def wavToMp4(self):
        wavDirPath = self.dirs['processedAudio'].dirPath
        mp4DirPath = self.dirs['streamAudio'].dirPath
        wavPath = f'{wavDirPath}/{self.fileName}.wav'
        mp4Path = f'{mp4DirPath}/{self.fileName}.mp4'
        audio = AudioSegment.from_file(wavPath)
        audio.export(mp4Path, format = 'mp4')
        self.streamPath = mp4Path

    async def addAudioEffects(self):
        fx = AudioEffectsChain()

        if self.reverse:
            fx.reverse()

        if self.speed != None:
            fx.speed(factor = self.speed)

        if self.reverb != None:
            fx.reverb(reverberance = self.reverb)
        
        if self.overdrive != None :
            fx.overdrive(gain = self.overdrive)

        wavDirPath = self.dirs['wavAudio'].dirPath
        processedDirPath = self.dirs['processedAudio'].dirPath
        wavPath = f'{wavDirPath}/{self.fileName}.wav'
        processedPath = f'{processedDirPath}/{self.fileName}.wav'

        fx(wavPath, processedPath)

    async def preStreamClean(self):
        self.dirs.preStreamClean(self.fileName)

    async def postStreamClean(self):
        self.dirs.postStreamClean(self.fileName)

if __name__ == '__main__':

    from dirs import Dirs

    dirs = Dirs()
    dirs.dirsSetup()

    searchTerm = input('What song would you like to search for? ')
    reverse = False
    speed = input('How much would you like to speed up the song? (1 = normal speed, 2 = double speed) ')
    reverb = input('How much reverb would you like to add? (0-100) ')
    overdrive = input('How much overdrive would you like to add? ')

    song = Song(
        dirs = dirs,
        searchTerm = searchTerm,
        reverse = reverse,
        speed = speed,
        reverb = reverb,
        overdrive = overdrive
    )
    song.processSong()
    print(song)