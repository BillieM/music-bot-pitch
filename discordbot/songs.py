import os
import shutil

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
    '''
    def __init__(self):
        pass

if __name__ == '__main__':

    searchTerm = input('What song would you like to search for? ')
    speedFactor = input('How much would you like to speed up the song? (1 = normal speed, 2 = double speed) ')
    reverbFactor = input('How much reverb would you like to add? (0-100) ')
    overdriveFactor = input('How much overdrive would you like to add? ')