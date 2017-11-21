'''
Created on 17 nov 2017

@author: koelio
'''

import ConfigParser
import os, errno

CONFIG_PATH = '..\config\config.cfg'

class DirectoryWriter(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_PATH)
        self.__config = config
        
    def createDir(self, directory):
      try:
        os.makedirs(self.__config.get('paths','cases') + '\\' + directory)
      except OSError as e:
        if e.errno != errno.EEXIST:
          raise    