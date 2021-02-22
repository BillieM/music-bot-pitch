import os
import shutil


class Dirs(dict):

    dirsConfig = {
        "downloadedAudio": {
            "requiresOnRunClean": False,
            "requiresPreStreamClean": False,
            "requiresPostStreamClean": False,
            "fileExtension": "mp4"
        },
        "wavAudio": {
            "requiresOnRunClean": True,
            "requiresPreStreamClean": True,
            "requiresPostStreamClean": False,
            "fileExtension": "wav"
        },
        "processedAudio": {
            "requiresOnRunClean": True,
            "requiresPreStreamClean": True,
            "requiresPostStreamClean": False,
            "fileExtension": "wav"
        },
        "streamAudio": {
            "requiresOnRunClean": True,
            "requiresPreStreamClean": False,
            "requiresPostStreamClean": True,
            "fileExtension": "mp4"
        }
    }

    def __init__(self):
        self.basePath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/audiofiles'

    def dirsSetup(self):
        self.configDirs()
        self.onRunClean()
        self.makeDirs()

    def configDirs(self):
        for dirName, dirConfig in zip(self.dirsConfig.keys(), self.dirsConfig.values()):
            dir = Dir(dirName, dirConfig, self.basePath)
            self[dirName] = dir

    def onRunClean(self):
        for dir in self.values():
            if dir.requiresOnRunClean and os.path.exists(dir.dirPath):
                shutil.rmtree(dir.dirPath)

    def preStreamClean(self, fileName):
        for dir in self.values():
            filePath = f'{dir.dirPath}/{fileName}.{dir.fileExtension}'
            if dir.requiresPreStreamClean and os.path.exists(filePath):
                os.remove(filePath)

    def postStreamClean(self, fileName):
        for dir in self.values():
            filePath = f'{dir.dirPath}/{fileName}.{dir.fileExtension}'
            if dir.requiresPostStreamClean and os.path.exists(filePath):
                os.remove(filePath)

    def makeDirs(self):
        for dir in self.values():
            if not os.path.exists(dir.dirPath):
                os.makedirs(dir.dirPath)

class Dir():

    def __init__(self, dirName, dirConfig, basePath):
        self.dirName = dirName
        self.dirPath = f'{basePath}/{dirName}'
        self.requiresOnRunClean = dirConfig['requiresOnRunClean']
        self.requiresPreStreamClean = dirConfig['requiresPreStreamClean']
        self.requiresPostStreamClean = dirConfig['requiresPostStreamClean']
        self.fileExtension = dirConfig['fileExtension']

    def __repr__(self):
        return f'{self.dirName} at {self.dirPath}'

    '''
    Class used for handling methods for individual dirs

    required method
        make necessary dir 

    '''

if __name__ == '__main__':
    dirs = Dirs()
    dirs.dirsSetup()
