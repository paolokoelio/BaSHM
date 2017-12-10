'''
Created on 07 nov 2017

@author: koelio
'''
import ConfigParser
import sys

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
      
    def open(self, path, mode="w"):  
      try:
        self.__f = open(self.__config.get('paths', 'cases') + path, mode)
      except IOError:
        print( "Could not read file: ", path)
        sys.exit()
        
    def write(self, data):
      try:
        self.__f.write(data)
      except IOError:
        print("Could write: ", data)
        sys.exit()
      
    def close(self):
      try:
        self.__f.close()
      except IOError:
        print("Could not close the file: ")
        sys.exit()
      
#     def createDir(self, directory):
#       try:
#         os.makedirs(self.__config.get('paths','cases') + '\\' + directory)
#       except OSError as e:
#         if e.errno != errno.EEXIST:
#           raise