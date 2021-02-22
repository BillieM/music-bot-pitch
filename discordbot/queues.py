class Queues(dict):
    def __init__(self, dirs):
        self.dirs = dirs 

    def getQueueObject(self, serverId):
        if serverId in self:
            queue = self[serverId]
        else:
            queue = Queue()
            self[serverId] = queue
        return queue

class Queue(list):
    def __init__(self):
        self.playing = False
        self.vc = None
        self.skip = False

    def __repr__(self):
        if len(self) > 0:
            queueItems = []
            for i, song in enumerate(self):
                if i == 0:
                    i = 'currently playing'
                queueItems.append(f'{i} - {song}')
            queueString = '\n💕💕💕 the queue 💕💕💕\n' + ''.join([f'\n{queueItem}\n' for queueItem in queueItems]) + '\n\n'
            return queueString
        else:
            return 'queue is empty! use #help for instructions to add songs to the queue'

    def addToQueue(self, song):
        self.append(song)
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