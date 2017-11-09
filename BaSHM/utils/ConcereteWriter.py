'''
Created on 07 nov 2017

@author: koelio
'''

import ConfigParser

CONFIG_PATH = '..\config\config.cfg'

class ConcreteWriter(object):
    '''
    Implementor of the Writer class for writing on text files
    '''
    __config = None
    __f = None

    def __init__(self):
      '''
      Constructor
      '''
      config = ConfigParser.ConfigParser()
      config.read(CONFIG_PATH)
      self.__config = config
      
    def open(self, path): 
      self.__f = open(self.__config.get('paths', 'cases') + path, "w")
        
    def write(self, data):
      self.__f.write(data)
      
    def close(self):
      self.__f.close()