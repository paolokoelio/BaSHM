'''
Created on 07 nov 2017

@author: koelio
'''
import ConfigParser
import os, errno


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
      
    #TODO esceptions handling  
    def open(self, path): 
      self.__f = open(self.__config.get('paths', 'cases') + path, "w")
        
    def write(self, data):
      self.__f.write(data)
      
    def close(self):
      self.__f.close()
      
    def createDir(self, directory):
      try:
        os.makedirs(self.__config.get('paths','cases') + '\\' + directory)
      except OSError as e:
        if e.errno != errno.EEXIST:
          raise
      
      # test
      #print(self.__config.get('paths','cases') + directory + 'successfully created')
   
#       # alternative solution
#       if not os.path.exists(directory):
#         os.makedirs(directory)
#       else: 
#         pass