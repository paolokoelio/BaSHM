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
#       part_desc = self.__partitions.get_mmls().get_desc()
#       
#       
#       print('Partition structure for: ' + part_desc + '\n')
#       print('{0:<2} {1:<30}\t{2:>15} {3:>15}\t{4:>15}\t{5:>7}'.format('#', 'Desc', 'Start sector', 'Start block', 'Length', 'Size'))
#       for part in self.__part_list:
# 
# #           entry = {'addr':part.addr, 'desc':part.desc, 'start':int(part.start), 'start512':int(part.start * 512), 'len':int(part.len)}
# #           list.append(entry)
#         #self.__part_list.append([part.addr, part.desc,part.start,part.start * self.__block_size,part.len,part.len * self.__block_size / (self.__factor)])
#         print('{:<2} {:<30}\t{:>15} {:>15}\t{:>15}\t{:>7} MB'.format(part[0],
#                                                                 part[1],
#                                                                 part[2],
#                                                                 part[3],
#                                                                 part[4],
#                                                                 part[5],
#                                                                 )
#               )
#         # print(part.addr, part.desc, "%ss(%s)" % (int(part.start), int(part.start * 512)), int(part.len)) #example alternative
#       print('\n')
      
      ch = raw_input(" >>  ")
      return self.exec_menu(ch)
    
    def timel(self):
      '''
      Perform timeline extraction
      '''
      print("Launching TSK fls module..\n")
      self.init_menu()
      #TODO put all arguments     
      
      print('YOYO {}'.format(self.__partitions.get_sel_offset()))
      self.__fls.set_offset(self.__partitions.get_sel_offset())
#      print(self.__partitions.get_sel_dev())
#       #test
#       print([self.__partitions.get_sel_dev()['DeviceID'].decode('unicode_escape')])
      
      self.__fls.set_images([self.__partitions.get_sel_dev()['DeviceID']])
      # we leave the rest default
      self.__fls.extractTimel()
    
      return
    
    def stimel(self):
      '''
      Perform super-timeline extraction
      '''
      print("Launching log2timeline module..\n")
      offset = self.init_menu()
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
      return self.__part_list[int(ch)][off_index]
    
    def exec_menu(self, ch):
      if ch == '':
          pass
      elif int(ch) == 0:
          return
      else:
          try:
              # set the offset of the corresponding partition
              offset = self.setOff(ch)
          except KeyError:
              print("Invalid selection, please try again.\n")
              pass
      return offset


    