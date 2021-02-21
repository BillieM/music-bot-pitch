import os
import shutil

dirsConfig = {
    "baseAudio": {
        "requiresOnRunClean": False
    },
    "wavAudio": {
        "requiresOnRunClean": True
    },
    "processedAudio": {
        "requiresOnRunClean": True
    },
    "streamAudio": {
        "requiresOnRunClean": True
    }
}

class Dirs(dict):

    def __init__(self):
        self.basePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/audiofiles'

    def configDirs(self, dirsConfig):
        for dirName, dirConfig in zip(dirsConfig.keys(), dirsConfig.values()):
            dir = Dir(dirName, dirConfig, self.basePath)
            self[dirName] = dir

    def cleanDirs(self):
        for dir in self.values():
            if dir.requiresOnRunClean and os.path.exists(dir.dirPath):
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

if __name__ == '__main__':
    dirs = Dirs()
    dirs.configDirs(dirsConfig)
    dirs.cleanDirs()
    dirs.makeDirs()
