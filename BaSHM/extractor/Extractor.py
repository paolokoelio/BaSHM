'''
Created on 10 nov 2017

@author: koelio
'''

from utils.ConcereteWriter import ConcreteWriter
from Fls import Fls
import sys, traceback
import ConfigParser  # import not compatible with python3, should be configparser
from partitions.Partitions import Partitions

CONFIG_PATH = '..\config\config.cfg'

class Extractor(object):
    '''
    classdocs
    '''
    __fls = None
    __devlist = None
    __config = None
    __partitions = None
    __mmls = None
    __part_list = None
    __offset = None

    def __init__(self, partitions):
      '''
      Constructor
      '''
      self.__partitions = partitions
        
      try:
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_PATH)      
        self.__config = config
      except Exception as e:
        sys.stderr.write(repr(e) + " in config file.\n")
        traceback.print_exc()
      
      self.__fls = Fls()
      
    def init_menu(self):
      
      # Exploiting the menu listing feature from Partitions()
      self.__partitions.init_menu()
      self.__part_list = self.__partitions.get_part_list()
      
      ch = raw_input(" >>  ")
      return self.exec_menu(ch)
    
    def timel(self):
      '''
      Perform timeline extraction
      '''
      print("Launching TSK fls module..\n")
      self.init_menu()
      
      #TODO put all arguments     
      self.__fls.set_offset(self.__offset)
      
      self.__fls.set_images([self.__partitions.get_sel_dev()['DeviceID']])
      # we leave the rest default, and launch fls
      self.__fls.extractTimel()
    
    
    def stimel(self):
      '''
      Perform super-timeline extraction
      '''
      print("Launching log2timeline module..\n")
      self.init_menu()
      #self.__l2t.run()
      
      return
    
    def browse(self):
      '''
      Browse the FS on the image
      '''
      print("This function is left for future work.")
      return
    
    def setOff(self, ch):
      
      # where offset in block is
      off_index = 3      
      self.__offset = self.__part_list[int(ch)][off_index]
    
    def exec_menu(self, ch):
      if ch == '':
          pass
      elif int(ch) == 0:
          return
      else:
          try:
              # set the offset of the corresponding partition
              self.setOff(ch)
          except KeyError:
              print("Invalid selection, please try again.\n")
              pass
      return 


    