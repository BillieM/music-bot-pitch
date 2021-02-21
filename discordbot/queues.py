class Queues(dict):
    def __init__(self, dirs):
        self.dirs = dirs 

    def getQueueObject(self.serverId):
        if serverId in self:
            queue = self[serverId]
        else:
            queue = Queue()
            self[serverId] = queue
        return queue

class Queue(list):

    '''
    modify this to use inheritance of a list
    '''

    def __init__(self):
        self.playing = False
        self.vc = None
        self.skip = False

    def __repr__(self):
        '''
        to add proper queue string
        '''
        return 'queue str here'

    def addToQueue(self, fileName, filePath, speed, reverb, overdrive, reversed):
        self.append({'name': fileName, 'path': filePath, 'speed': speed, 'reverb': reverb, 'overdrive': overdrive, 'reversed': reversed})
        return self[-1]

    def removeCurrentSong(self):
        self.pop(0)

    def getNextSong(self):
        nextSong = self[0]

        return nextSong

    def isNextSong(self):
        if len(self) > 0:
            return True
        else:
            return False

    def getQueueString(self):
        if len(self) > 0:
            queueItems = []
            for i, song in enumerate(self):
                songString = getSongString(song)
                if i == 0:
                    i = "currently playing"
                queueItems.append(f'{i} - {songString}')
            queueString = '\n💕💕💕 the queue 💕💕💕\n' + ''.join([f'\n{queueItem}\n' for queueItem in queueItems]) + '\n\n'
            return queueString
        else:
            return "queue is empty! use #play to add to queue"