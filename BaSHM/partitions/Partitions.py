'''
Created on 13 nov 2017

@author: koelio
'''

import subprocess as sp
import re
from partitions.Mmls import Mmls
from utils.ConcereteWriter import ConcreteWriter

class Partitions(object):
    '''
    Handles logical structure information of a device
    '''
    __devlist = None
    __devices = None
    __mmls = None
    __config = None
    _selDev = None
    __selOffset = 0
    __part_list = None
    __choice = None
    __suffix = '_disk_data.txt'

    def __init__(self, config):
      '''
      Constructor
      '''     
      self.__config = config
      self.__writer = ConcreteWriter()
        
    def init_menu(self):
      
      print('Choose a device:\n')

      self.print_menu()
      
      ch = raw_input(" >>  ")
      self.exec_menu(ch)

    def getPartInfo(self):

      self.print_menu()
      ch = raw_input(" >>  ")
      self.exec_menu(ch)
      out = self.runMmls()

      self.writeInfo(out, self._selDev)

    def getDevices(self):
      
      cmd = ''.join([self.__config.get('commands', 'physicaldevice')])
      
      out = self.run_cmd(cmd)

      devices = self.parse_out(out)

      # this commented piece of code tries to match the serial numbers of devices
      # to their DeviceID (i.e. \\.\physicaldrive*), but for consistency reasons
      # it has been commented and abbandoned
      # cmd = ''.join([self.__config.get('commands', 'physicalmedia')])
      
      # out = self.run_cmd(cmd)

      # physicalMedia = self.parse_out(out)

      # new_device_list =[]
      # for device in devices:
      #   for medium in physicalMedia:
      #     if str(medium['Tag']) in str(device['DeviceID']):
      #       device['SerialNumber'] = medium['SerialNumber']

      return devices
 
    def print_menu(self):
      
      self.__devlist = self.getDevices()
      # self.__devlist = self.__devices
      
      i = 1
      for device in self.__devlist:
        print("%d . %s DevID: %s #partitions: %s" % (
            i, device['Model'], device['DeviceID'], device['Partitions']))
        i = i + 1
      # print (self.__menu_devs)
      
    def parse_out(self, out):
      
      # split per device, quite fragile as a condition, but as long as PowerShell result is consistent we're ok
      out = re.split("\r\n\r\n", out)
      # filter empty elements
      disks = filter(None, out)

      out = []
      for disk in disks:  
        result = {}
        for row in disk.split('\n'):
            if ': ' in row:
                key, value = row.split(': ')
                result[key.strip(' .')] = value.strip()
        out.append(result)

      return out
    
    def runMmls(self):
      ch = self.__choice
      self.__mmls = Mmls()
      self.__mmls.set_dev_path(self.__devlist[int(ch) - 1]['DeviceID'])
      self.__mmls.set_desc(str(self.__devlist[int(ch) - 1]['Model']))
      
      return self.__mmls.mmls()
    
#   TODO future work open shell with typed mmls (allows for original use of mmls)    
    def openShell(self):
      return
    
    def writeInfo(self, par_list, sel_dev):
      # set pathname for extracting the timeline
      model = str(sel_dev['Model']).replace(' ', '')
      model = model.replace('USBDevice', '')
      directory = str('case_' + model)
      filename = self.__config.get('paths', 'cases') + '\\' + directory + '\\' + model + self.__suffix

      out = '\nPartition structure for ' + model + ':\n'
      out = out + '{0:<2} {1:<30}\t{2:>15} {3:>15}\t{4:>15}\t{5:>7}\n'.format('#', 'Desc', 'Start sector', 'Start block', 'Length', 'Size')

      for part in par_list:
        out = out + '{:<2} {:<30}\t{:>15} {:>15}\t{:>15}\t{:>7} MB\n'.format(part[0],part[1],part[2],part[3],part[4],part[5])

      self.__writer.open(filename, "a")
      self.__writer.write(out)
      self.__writer.close()

    def exec_menu(self, ch):
        if ch == '':
            pass
        elif int(ch) == 0:
            return
        else:
            try:
                # select a device and get it's list partition by running mmls
                self.__choice = ch
                self._selDev = self.__devlist[int(ch) - 1]
#                 self.__part_list = self.runMmls(ch)
            except KeyError:
                print("Invalid selection, please try again.\n")
            except IndexError:
                print("Out of index, please choose frome the list again.\n")
                self.init_menu()

    def run_cmd(self, cmd):
      '''
        Prints and runs specified command
      '''
      print('Issuing command: "' + str(''.join(cmd)) + '".')
      
      try:
          out = sp.check_output(cmd,
            # stdout=sp.STDOUT,
            stderr=sp.STDOUT,
            shell=True)
          print('\n')
      except sp.CalledProcessError as e:
          print("\nSomething went wrong. You may retry this action." + " ret_code: " + str(e.returncode) + "\n")
      
      return out
    
    def get_devlist(self):
      
      self.__devlist  = self.getDevices()
      return self.__devlist    

    def get_sel_dev(self):
      return self._selDev

    def set_sel_dev(self, value):
      self._selDev = value
      
    def get_sel_offset(self):
      return self.__selOffset

    def set_sel_offset(self, value):
      self.__selOffset = value

    def get_mmls(self):
      return self.__mmls    
    
    def get_part_list(self):
      return self.__part_list
