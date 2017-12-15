'''
Created on 07 nov 2017

@author: koelio
'''

class Writer(object):
    '''
    Abstract Writer for writing data on file TODO implement bridge
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def open(self, path):
        raise NotImplementedError("Subclass must implement abstract method")
      
    def write(self, data):
        raise NotImplementedError("Subclass must implement abstract method")
      
    def close(self):
        raise NotImplementedError("Subclass must implement abstract method")