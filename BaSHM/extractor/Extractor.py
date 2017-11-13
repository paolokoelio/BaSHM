'''
Created on 10 nov 2017

@author: koelio
'''

from utils.ConcereteWriter import ConcreteWriter
from Fls import Fls


class Extractor(object):
    '''
    classdocs
    '''
    __fls = None

    def __init__(self):
      '''
      Constructor
      '''
      self.__fls = Fls()
      
    def init_menu(self):
      
      print('Choose the device to scan:\n')
      self.__devlist = None
      
      i = 1
      for device in self.__devlist.devices:
        
#         self.__menu_devs[i] = "mod:%s sn:%s, %s device on /dev/%s" % (
#             device.model, device.serial, device.interface.upper(), device.name)

        print( "%d. %s serial:%s, %s device on /dev/%s" % (
            i, device.model, device.serial, device.interface.upper(), device.name) )
        
        i = i + 1
      #print (self.__menu_devs)
      
      ch = raw_input(" >>  ")
      self.exec_menu(ch)
    
    def timel(self):
      '''
      Perform timeline extraction
      '''
      print("Launching TSK fls module..\n")
      self.__fls.extractTimel()
    
      return
    
    def stimel(self):
      '''
      Perform super-timeline extraction
      '''
      
      
      return
    
    def browse(self):
      '''
      Browse the FS on the image
      '''
      print("This function is left for future work.")
      return