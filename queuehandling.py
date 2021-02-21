
def getSongString(songDict):
    '''
    move this function to the __repr__ method of the Song() class
    '''
    songTitle = songDict['name']

    if songDict['reversed']:
        songTitle = songTitle[::-1]

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

    '''
    modify this to use inheritance of a list
    '''

    def __init__(self):
        self.queueList = []
        self.playing = False
        self.vc = None
        self.skip = False

    def addToQueue(self, fileName, filePath, speed, reverb, overdrive, reversed):
        self.queueList.append({'name': fileName, 'path': filePath, 'speed': speed, 'reverb': reverb, 'overdrive': overdrive, 'reversed': reversed})
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
