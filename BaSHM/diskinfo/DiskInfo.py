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
    Manages objects related to Disk Health through pySMART wrapper for smartmontools (https://www.smartmontools.org/)
    '''
    
    __devlist = None
    __device = None
    __writer = None
    __dir_writer = None
    __menu_devs = {}
    __f_name = 'disk_data.txt'
    __sel_model = ''
    __directory = ''

    def __init__(self, partitions):
        '''
        Constructor
        '''
        self.__partitions = partitions

        self.__writer = ConcreteWriter()
        self.__dir_writer = DirectoryWriter()
        
    def init_menu(self):
      # initialize menu and choice selection
      self.printMenu()
            
      ch = raw_input(" >>  ")
      self.exec_menu(ch)  
    
    def chkhealth(self, device):

      # self.__model has the correct value only if the createCaseFolder
      # method has been first called, and it stays valid only in the same instance;
      # this may, if the case_folder already exists and you have re-run the application
      # checkhealth will not work if not calling createCaseFolder before,
      # thus we force its call here:
      self.createCaseFolder()

      try:

        self.__f_name = str(self.__directory + '\\' + self.__sel_model + '_' + self.__f_name)
    
        # write to directory 
        self.__writer.open(self.__f_name)
        print("\n")

        out = 'Device Data:' + '\n'  + 'mod: ' + str(device.model) + ', sn: ' + str(device.serial) + ', MD5: TODO ' + 'name: ' + str(device.name) # TODO hash
        print(out)
        self.__writer.write(out)

        out = "\nSMART check for " + str(device.model) + '(' + str(device.name) + "):\n"
        print(out)
        
        self.__writer.write(out)
        
        out = str(device.assessment) + "\n"
        print(out)
        
        self.__writer.write(out + "\n")
        
        # after helath check, print all attributes
          
        header_printed = False
        for attr in device.attributes:
            if attr is not None:
                if not header_printed:
                    self.__writer.write("{0:>3} {1:24}{2:4}{3:4}{4:4}{5:9}{6:8}{7:12}"
                          "{8}\n".format(
                              'ID#', 'ATTRIBUTE_NAME', 'CUR', 'WST', 'THR',
                              'TYPE', 'UPDATED', 'WHEN_FAIL', 'RAW'))
                    header_printed = True
                self.__writer.write(str(attr) + "\n")
        if not header_printed:
            print("This device does not support SMART attributes.")
          
        self.__writer.close()
        # flush name values
        self.__f_name = 'disk_data.txt'
        self.__directory = ''

      except IOError as io:
        # traceback.print_exc()
        print("Consider creating a case directory first.\n{} \n".format(io))    
        return 2

    def createCaseFolder(self):
      # creates specific case folder w.r.t. drive name
      print('\n')
      print("You need to create a directory for the device data.\n")
      self.__partitions.init_menu()
      

      # self.__part_list = self.__partitions.get_part_list()
      sel_dev = self.__partitions.get_sel_dev()

      model = str(sel_dev['Model']).replace(' ', '')
      model = model.replace('USBDevice', '')
      self.__sel_model = model

      ch = raw_input(" >> {}{}{}".format('cases\\', 'case_', self.__sel_model)) or ('case_' + str(self.__sel_model))

      print('\n')
      self.__directory = str(ch).replace(' ', '')
      self.__directory.replace('USBDevice', '')
      self.__dir_writer.createDir(self.__directory)
      # self.__writer.createDir(directory)
  
    def openDD(self):
      # future work TODO
      pass

    def printMenu(self):
      # prints menu entries      
      print('Loading devices...')
      self.__devlist = DeviceList()
      print('Choose the device to test:\n')
      i = 1
      new_devices = []

      for device in self.__devlist.devices:
          # reordering the list for consistency
          new_devices.append(device)
          print("%d. %s sn:%s, %s device on %s" % (
              i, device.model, device.serial, device.interface.upper(), device.name))
          i = i + 1
      print('\n')
      self.__devlist.devices = new_devices
      
    def exec_menu(self, ch):
      # executes the selected action in menu
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
                print("Invalid selection, please try again. \n")
                traceback.print_exc() 
                
        return
