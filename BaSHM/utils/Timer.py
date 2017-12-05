import time

class Timer(object):
    '''
    Set timer for logging
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.startTime = 0
        self.endTime = 0
        self.duration = 0

    def start(self):
        self.startTime = time.time()

    def stop(self):
        self.endTime=time.time()

    def printDuration(self):
        self.duration = self.endTime - self.startTime
        print("\nElapsed Time: {0:.2f} seconds\n".format(round(self.duration,2)))

    def getDuration(self):
        return self.duration

