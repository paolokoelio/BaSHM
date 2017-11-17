'''
Created on 27 ott 2017

@author: koelio
'''

from __future__ import print_function
from pySMART import DeviceList  # smartmontools wrapper
from utils.ConcereteWriter import ConcreteWriter


class DiskInfo(object):
    '''
    Class for managing objects related to Disk Health through pySMART wrapper for smartmontools (https://www.smartmontools.org/)
    '''
    
    __devlist = None
    __device = None
    __writer = None
    __menu_devs = {}
    __f_name = 'disk_data.txt'

    def __init__(self):
        '''
        Constructor
        '''
        self.__writer = ConcreteWriter()
        
    def init_menu(self):
      
      print('Choose the device to test:\n')
      self.__devlist = DeviceList()
      
      i = 1
      for device in self.__devlist.devices:
        
#         self.__menu_devs[i] = "mod:%s sn:%s, %s device on /dev/%s" % (
#             device.model, device.serial, device.interface.upper(), device.name)

        print("%d. %s serial:%s, %s device on /dev/%s" % (
            i, device.model, device.serial, device.interface.upper(), device.name))
        
        i = i + 1
      # print (self.__menu_devs)
      
      ch = raw_input(" >>  ")
      self.exec_menu(ch)
    
    def initialize(self):
      self.init_menu()
        
    # TODO exception handling   
    def chkhealth(self, device):
      
      self.__writer.open(self.__f_name)
      print("\n")
      
      out = 'Devie Data:' + '\n' + 'name: ' + str(device.name) + ', mod: ' + str(device.model) + ', sn: ' + str(device.serial) + ', MD5: '  # TODO hash
      print(out)
      self.__writer.write(out)
      # optionally? print all attributes
      # device.all_attributes() 
      out = "\nSMART check for /dev/" + str(device.name) + " " + str(device.model) + ":\n"
      print(out)
      self.__writer.write(out)
      
      out = str(device.assessment) + "\n"
      print(out)
      
      self.__writer.write(out)
      self.__writer.close()

    def createCaseFolder(self):
      
      # print (self.__menu_devs)
      print('Choose the device(s) of the case\n')
      self.__devlist = DeviceList()
      
      i = 1
      for device in self.__devlist.devices:
        print("%d. %s serial:%s, %s device on /dev/%s" % (
            i, device.model, device.serial, device.interface.upper(), device.name))
        i = i + 1
      
      
      ch = raw_input(" >> ")
      if int(ch) == 0: 
        return
      else:
        out  =self.__devlist.devices[int(ch) - 1].model
        ch = raw_input(" >> {}{}{}".format('cases\\', 'case_', str(out))) or ('case_' + str(out))

      
      directory = str(ch).replace(' ', '_')
      self.__writer.createDir(directory)

  
    def openDD(self):
      pass
      
    def exec_menu(self, ch):
        if ch == '':
            pass
        elif int(ch) == 0:
            return
        else:
            try:
                # select the device to test, -1 because in menu prints at 1
                self.__device = self.__devlist.devices[int(ch) - 1]
                self.chkhealth(self.__device)
            except KeyError:
                print("Invalid selection, please try again.\n")
                pass
        return
