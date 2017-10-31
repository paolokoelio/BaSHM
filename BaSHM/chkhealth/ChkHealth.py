'''
Created on 27 ott 2017

@author: koelio
'''

from pySMART import DeviceList, Device


class ChkHealth(object):
    '''
    Class for managing objects related to Disk Health through pySMART wrapper for smartmontools (https://www.smartmontools.org/)
    '''
    
    __devlist = None

    def __init__(self):
        '''
        Constructor
        '''
        
    def dev_menu(self):
      
      
      pass   
        
    def chkhealth(self):
      
      self.__devlist = DeviceList()
      
      print(self.__devlist)
      
      #print("Device 2:\n" + str(self.__devlist.devices[1].all_attributes()))
      
      print("Device 2: " + str(self.__devlist.devices[1]) + "\nSMART check result: \n" + str(self.__devlist.devices[1].assessment))
      
      