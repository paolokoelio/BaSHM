'''
Created on 13 nov 2017

@author: koelio
'''

import subprocess as sp
import ConfigParser
import re


class Partitions(object):
    '''
    Handles logical structure information of a device
    '''

    __device = None

    def __init__(self):
        '''
        Constructor
        '''
  
    def init_menu(self):
      
      print('Choose a device:\n')
      self.__devlist = None
      
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
    
    def getInfo(self):
      
      # TODO put in config.cfg
      cmd = ['powershell.exe',
            'Get-WmiObject Win32_DiskDrive', '| format-list']
      out = self.run_cmd(cmd)

      self.parse_out(out)
      
    def parse_out(self, out):
      
      # split per device
      out = re.split("\r\n\r\n", out)
      # filter empty elements
      disks = filter(None, out)
      #print(disks)
      
#       i = 0
#       for i in range(len(disks)):  # quite fragile as a condition, but as long as powerShell result is consistent we're ok
#         print(disks[i])
#         i = i + 1
#         print('yo')
      
#       for disk in disks:  # quite fragile as a condition, but as long as powerShell result is consistent we're ok
#         print(disk)
#         print('yo')

      tmp = []
      i = 0
      for i in range(len(disks)):  # quite fragile as a condition, but as long as powerShell result is consistent we're ok
        #print(disks[i])
        result={}
        for row in disks[i].split('\n'):
            if ': ' in row:
                key, value = row.split(': ')
                result[key.strip(' .')] = value.strip()
        tmp.append(result)
        print(result)

      #print(tmp)  
      #print(disks)
    
    def exec_menu(self, ch):
        if ch == '':
            pass
        elif ch == 0:
            self.getInfo()
        else:
            try:
                # select the device to test, -1 because in menu prints at 1
                self.__device = self.__devlist.devices[int(ch) - 1]
                self.getInfo(self.__device)
            except KeyError:
                print("Invalid selection, please try again.\n")
                pass
        return

    def run_cmd(self, cmd):
      '''
        Prints and runs specified command
      '''
      print('Needs to be run as Privileged User.')
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
