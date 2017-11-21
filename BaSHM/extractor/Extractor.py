'''
Created on 10 nov 2017

@author: koelio
'''

from Fls import Fls


class Extractor(object):
    '''
    classdocs
    '''
    __fls = None
    __l2t = None
    __devlist = None
    __config = None
    __partitions = None
    __mmls = None
    __part_list = None  # partition list of the selected device in Partition during menu choice
    __sel_dev = None  # device selected in Partition class during menu choice
    __offset = None

    def __init__(self, config, partitions):
      '''
      Constructor
      '''
      self.__partitions = partitions
      self.__config = config
      self.__fls = Fls()
      
    def init_menu(self):
      
      # Exploiting the menu listing feature from Partitions()
      self.__partitions.init_menu()
      self.__part_list = self.__partitions.get_part_list()
      self.__sel_dev = self.__partitions.get_sel_dev()
      
      ch = raw_input(" >>  ")
      self.exec_menu(ch)
    
    def timel(self):
      '''
      Perform timeline extraction
      '''
      print("Launching fls module..\n")
      self.init_menu()
         
      self.__fls.set_offset(self.__offset)
      
      # set pathname for extracting the timeline
      directory = str('case_' + str(self.__sel_dev['Model'])).replace(' ', '_')
      self.__fls.set_filename(self.__config.get('paths', 'cases') + '\\' + directory + '\\' + 'body.txt')
      
      # set the physical device
      self.__fls.set_images([self.__partitions.get_sel_dev()['DeviceID']])
      
      # we leave the rest default, and launch fls (TODO: set timer)
      if self.__fls.extractTimel() == 0:
        print("Success!")
      else:
        print("Uh-oh")
    
    def stimel(self): #TODO delete this
      '''
      Perform super-timeline extraction
      '''
      print("Launching log2timeline module..\n")
      self.init_menu()
      
      self.__l2t.setOffset(self.__offset)
      
      directory = str('case_' + str(self.__sel_dev['Model'])).replace(' ', '_')
      self.__fls.set_filename(self.__config.get('paths', 'cases') + '\\' + directory + '\\' + 'super_timel.csv')
      
      # self.__l2t.setogffset(self.__offset)
      # self.__l2t.run()
      
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
      # print('{}'.format(self.__part_list[int(ch)]))
      self.__offset = int(self.__part_list[int(ch)][off_index])
    
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

