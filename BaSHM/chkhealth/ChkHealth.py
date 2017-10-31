'''
Created on 27 ott 2017

@author: koelio
'''

from __future__ import print_function
from pySMART import DeviceList, Device



class ChkHealth(object):
    '''
    Class for managing objects related to Disk Health through pySMART wrapper for smartmontools (https://www.smartmontools.org/)
    '''
    
    __devlist = None
    __menu_devs = {}

    def __init__(self):
        '''
        Constructor
        '''
        
    def init_menu(self):
      
      print('Choose the device to test:\n')
      self.__devlist = DeviceList()
      
      i = 1
      for device in self.__devlist.devices:
        self.__menu_devs[i] = "mod:%s sn:%s, %s device on /dev/%s" % (
            device.model, device.serial, device.interface.upper(), device.name)

#         print( "%d mod:%s sn:%s %s device on /dev/%s" % (
#             i, device.model, device.serial, device.interface.upper(), device.name) )
        
        i = i + 1
      print (self.__menu_devs)
    
    def initialize(self):
      pass
        
    def chkhealth(self):
      
      self.init_menu()
      #print(self.__devlist)
      
      #print("Device 2:\n" + str(self.__devlist.devices[1].all_attributes()))
      
      print("Device 2: " + str(self.__devlist.devices[1]) + "\nSMART check result: \n" + str(self.__devlist.devices[1].assessment))
      
      