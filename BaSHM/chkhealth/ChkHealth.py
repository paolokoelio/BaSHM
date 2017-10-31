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
    __device = None
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
        
#         self.__menu_devs[i] = "mod:%s sn:%s, %s device on /dev/%s" % (
#             device.model, device.serial, device.interface.upper(), device.name)

        print( "%d. %s serial:%s, %s device on /dev/%s" % (
            i, device.model, device.serial, device.interface.upper(), device.name) )
        
        i = i + 1
      #print (self.__menu_devs)
      
      ch = raw_input(" >>  ")
      self.exec_menu(ch)
    
    def initialize(self):
      self.init_menu()
        
    def chkhealth(self, device):
      
      print("\n")
      #TODO print device information
      
      #optionally? print alla attributes
      #device.all_attributes()
      
      print("\nSMART check for /dev/" +str(device.name) + " " + str(device.model) + ":")
      print(" " + str(device.assessment) + "\n")
      
    def exec_menu(self, ch):
        if ch == '':
            pass
        elif ch == 0:
            self.chkhealth()
        else:
            try:
                #select the device to test, -1 because in menu prints at 1
                self.__device = self.__devlist.devices[int(ch)-1]
                self.chkhealth(self.__device)
            except KeyError:
                print("Invalid selection, please try again.\n")
                pass
        return