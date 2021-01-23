from pytube import YouTube
import os
from youtubesearchpython import VideosSearch
from pprint import pprint
from pysndfx import AudioEffectsChain
import random
from string import ascii_letters
import time
from pydub import AudioSegment
import sox

def generateFileName():
    random.seed(time.time())
    fileName = ''.join(random.choice(ascii_letters) for _ in range(10))
    return fileName

def getUrlFromSearchTerm(searchTerm):

    videosSearch = VideosSearch(searchTerm, limit = 1)

    videoTitle = videosSearch.result()['result'][0]['accessibility']['title'] 
    videoUrl = videosSearch.result()['result'][0]['link']

    return videoUrl, videoTitle

def downloadAudioFromYoutube(url, fileName):

    try:
        yt = YouTube(url)
        audioStream = yt.streams.filter(only_audio=True).first()
        audioStream.download(youtubeDir, filename=fileName)
        return True

    except Exception as e:
        return False

def mp4ToWav(fileName):
    inPath = f'{youtubeDir}/{fileName}.mp4'
    outPath = f'{wavDir}/{fileName}.wav'
    audio = AudioSegment.from_file(inPath)
    audio.export(outPath, format = 'wav')

def wavToMp4(fileName):
    inPath = f'{processedDir}/{fileName}.wav'
    outPath = f'{streamDir}/{fileName}.mp4'
    audio = AudioSegment.from_file(inPath)
    audio.export(outPath, format = 'mp4')

def addAudioEffects(fileName, speedFactor, reverbFactor):
    fx = (
        AudioEffectsChain().speed(speedFactor).reverb(reverberance=reverbFactor)
    )

    inFile = f'{wavDir}/{fileName}.wav'
    outFile = f'{processedDir}/{fileName}.wav'

    fx(inFile, outFile)

def cleanDirs():
    for file in os.listdir(youtubeDir):
        path = f'{youtubeDir}/{file}'
        os.unlink(path)
    for file in os.listdir(wavDir):
        path = f'{wavDir}/{file}'
        os.unlink(path)
    for file in os.listdir(processedDir):
        path = f'{processedDir}/{file}'
        os.unlink(path)

def makeDirs():
    if not os.path.exists(youtubeDir):
        os.makedirs(youtubeDir)    
    
    if not os.path.exists(wavDir):
        os.makedirs(wavDir)

    if not os.path.exists(processedDir):
        os.makedirs(processedDir)

    if not os.path.exists(streamDir):
        os.makedirs(streamDir)

pathDir = os.path.abspath(os.path.dirname(__file__))
youtubeDir = f'{pathDir}/downloadedAudio'
wavDir = f'{pathDir}/wavAudio'
processedDir = f'{pathDir}/processedAudio'
streamDir = f'{pathDir}/streamAudio'

print(pathDir, youtubeDir, wavDir, processedDir, streamDir)

def main(searchTerm, speedFactor = 1, reverbFactor = 40):
    dirs = makeDirs()
    fileName = generateFileName()
    youtubeUrl, songTitle = getUrlFromSearchTerm(searchTerm)
    downloadSuccess = downloadAudioFromYoutube(youtubeUrl, fileName)
    convertToWav = mp4ToWav(fileName)

    audioEffects = addAudioEffects(fileName, speedFactor, reverbFactor)
    convertToMp4 = wavToMp4(fileName)
    cleanup = cleanDirs()

    return fileName, songTitle

if __name__ == '__main__':

    searchTerm = input("what search term? ")
    speedFactor = input("what speed factor? (2 = double speed) ")
    reverbFactor = input("what reverb factor? (0-100) ")

    main(searchTerm, speedFactor, reverbFactor)