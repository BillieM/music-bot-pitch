import os
import shutil

'''
may also move the dir classes to a seperate file
maybe dir object is defined with the queue???
'''

dirsConfig = {
    'baseAudio': {
        'requiresOnRunClean': False
    },
    'wavAudio': {
        'requiresOnRunClean': True
    },
    'processedAudio': {
        'requiresOnRunClean': True
    },
    'streamAudio': {
        'requiresOnRunClean': True
    }
}

class Song():

    '''
    Class used for downloading songs/ processing audio

    required methods
        get song url from search term
        extract information from videosearch object
        check if song already downloaded
        download song from youtube
        convert mp4 to wav
        convert wav to mp4
        add audioeffects

    also note, right now stream audio files are stacking up
        these should be deleted on stream finish
    '''
    def __init__(self):
        pass

class Dirs(dict):

    def __init__(self):
        self.basePath = os.path.abspath(os.path.dirname(__file__))

    def configDirs(self, dirsConfig):
        for dirName, dirConfig in zip(dirsConfig.keys(), dirsConfig.values()):
            dir = Dir(dirName, dirConfig, self.basePath)
            self[dirName] = dir

    def cleanDirs(self):
        for dir in self.values():
            if dir.requiresOnRunClean:
                shutil.rmtree(dir.dirPath)

    def makeDirs(self):
        for dir in self.values():
            if not os.path.exists(dir.dirPath):
                os.makedirs(dir.dirPath)

class Dir():

    def __init__(self, dirName, dirConfig, basePath):
        self.dirName = dirName
        self.dirPath = f'{basePath}/{dirName}'
        self.requiresOnRunClean = dirConfig['requiresOnRunClean']

    def __repr__(self):
        return f'{self.dirName} at {self.dirPath}'

    '''
    Class used for handling methods for individual dirs

    required method
        make necessary dir 

    '''

def onLaunch():
    dirs = Dirs()
    dirs.configDirs(dirsConfig)
    dirs.cleanDirs()
    dirs.makeDirs()

def processSong(
    searchTerm, 
    speedFactor = 1,
    reverbFactor = 0,
    overdriveFactor = 0,
):

    song = Song()

if __name__ == '__main__':

    searchTerm = input('What song would you like to search for? ')
    speedFactor = input('How much would you like to speed up the song? (1 = normal speed, 2 = double speed) ')
    reverbFactor = input('How much reverb would you like to add? (0-100) ')
    overdriveFactor = input('How much overdrive would you like to add? ')
    
    onLaunch()

    processSong(
        searchTerm = searchTerm,
        speedFactor = speedFactor,
        reverbFactor = reverbFactor,
        overdriveFactor = overdriveFactor
    ) 