'''
Created on 27 ott 2017

@author: koelio
'''

from __future__ import print_function
import traceback
from pySMART import DeviceList  # smartmontools wrapper
from utils.ConcereteWriter import ConcreteWriter
from utils.DirectoryWriter import DirectoryWriter


class DiskInfo(object):
    '''
    Class for managing objects related to Disk Health through pySMART wrapper for smartmontools (https://www.smartmontools.org/)
    '''
    
    __devlist = None
    __device = None
    __writer = None
    __dir_writer = None
    __menu_devs = {}
    __f_name = 'disk_data.txt'

    def __init__(self, partitions):
        '''
        Constructor
        '''
        self.__partitions = partitions

        self.__writer = ConcreteWriter()
        self.__dir_writer = DirectoryWriter()
        
    def init_menu(self):
      
      self.printMenu()
            
      ch = raw_input(" >>  ")
      self.exec_menu(ch)  
    
    def chkhealth(self, device):

      #create directory if it doesn't exist
      model = str(device.model).replace(' ', '_')
      directory = 'case_' + model
      self.__dir_writer.createDir(directory)
      self.__f_name = str(directory + '\\' + model + '_' + self.__f_name)
      #print(self.__f_name)
  
      #write to directory 
      self.__writer.open(self.__f_name)
      print("\n")

      out = 'Device Data:' + '\n' + 'name: ' + str(device.name) + ', mod: ' + str(device.model) + ', sn: ' + str(device.serial) + ', MD5: TODO'  # TODO hash
      print(out)
      self.__writer.write(out)

      out = "\nSMART check for " + str(device.name) + " " + str(device.model) + ":\n"
      print(out)
      
      self.__writer.write(out)
      
      out = str(device.assessment) + "\n"
      print(out)
      
      self.__writer.write(out + "\n")
      
      # after test print all attributes
        
      header_printed = False
      for attr in device.attributes:
          if attr is not None:
              if not header_printed:
                  self.__writer.write("{0:>3} {1:24}{2:4}{3:4}{4:4}{5:9}{6:8}{7:12}"
                        "{8}\n".format(
                            'ID#', 'ATTRIBUTE_NAME', 'CUR', 'WST', 'THR',
                            'TYPE', 'UPDATED', 'WHEN_FAIL', 'RAW'))
                  header_printed = True
              self.__writer.write(str(attr)+"\n")
      if not header_printed:
          print("This device does not support SMART attributes.")
        
      self.__writer.close()
      #flush filename
      self.__f_name = 'disk_data.txt'

    def createCaseFolder(self):
      self.printMenu()
      print('\n')
      
      ch = raw_input(" >> ")
      if int(ch) == 0: 
        return
      else:
        out = self.__devlist.devices[int(ch) - 1].model
        ch = raw_input(" >> {}{}{}".format('cases\\', 'case_', str(out))) or ('case_' + str(out))

      print('\n')
      directory = str(ch).replace(' ', '_')
      self.__dir_writer.createDir(directory)
      #self.__writer.createDir(directory)
  
    def openDD(self):
      pass

    def printMenu(self):
      
      # needed for consistency between names, i.e. /dev/sda and \\.\.physicaldrive0
      self.__windev = self.__partitions.get_devlist()
      #print(self.__windev)
      
      print('Loading devices...')
      self.__devlist = DeviceList()
      print('Choose the device:\n')
      i = 1
      new_devices = []
      for windev in self.__windev:
        for device in self.__devlist.devices:
          if str(windev['Model']) in str(device.model):
            device.name = windev['DeviceID']
            #reordering the list for consistency
            new_devices.append(device)
            print("%d. %s serial:%s, %s device on %s" % (
                i, device.model, device.serial, device.interface.upper(), device.name))
            i = i + 1
      print('\n')
      self.__devlist.devices = new_devices
      
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
            except IndexError:
                print("Invalid selection, please try again. YO\n")
                traceback.print_exc() 
                
        return
