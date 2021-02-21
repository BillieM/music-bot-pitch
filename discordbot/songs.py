import os
import shutil
from youtubesearchpython import VideosSearch

'''
may also move the dir classes to a seperate file
maybe dir object is defined with the queue???
i think dirs object is created on run, & then passed to each queue instance
'''

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

    and... also need to add error handling (with understandable messages sent back to discord)
    
    ideally want to use multithreading for this whole process (definitely for download)
    '''
    def __init__(self, dirs, searchTerm, speed = 1, reverb = 0, overdrive = 0):
        self.dirs = dirs
        self.searchTerm = searchTerm
        self.speed = speed
        self.reverb = reverb
        self.overdrive = overdrive
        self.videoSearch = None
        self.title = None
        self.duration = None
        self.url = None

    def __repr__(self):
        '''
        changes from old version will be
            remove unnecessary info
            show song length before & song length after

        '''
        return f'{self.searchTerm}, {self.speed}, {self.reverb}, {self.overdrive} -> {self.title}, {self.url}, {self.duration}'

    def processSong(self):
        self.getVideoSearchObject()
        self.extractInfoFromVideoSearch()

    def getVideoSearchObject(self):
        '''
        retry 3x
        '''
        for i in range(3):
            try:
                videoSearch = VideosSearch(searchTerm, limit = 3).result()
                self.videoSearch = videoSearch['result'][i]
                break
            except Exception as e:
                print('failure')
        
    def extractInfoFromVideoSearch(self):
        self.title = self.videoSearch['title']
        self.duration = self.videoSearch['duration']  
        self.url = self.videoSearch['link']

if __name__ == '__main__':

    from dirs import Dirs

    dirs = Dirs()

    searchTerm = input('What song would you like to search for? ')
    speed = input('How much would you like to speed up the song? (1 = normal speed, 2 = double speed) ')
    reverb = input('How much reverb would you like to add? (0-100) ')
    overdrive = input('How much overdrive would you like to add? ')

    song = Song(
        dirs = dirs,
        searchTerm = searchTerm,
        speed = speed,
        reverb = reverb,
        overdrive = overdrive
    )
    song.processSong()
    print(song)