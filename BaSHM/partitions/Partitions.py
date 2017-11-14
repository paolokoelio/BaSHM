'''
Created on 13 nov 2017

@author: koelio
'''

import subprocess as sp
import re, sys, traceback
from partitions.Mmls import Mmls
import ConfigParser  # import not compatible with python3, should be configparser

CONFIG_PATH = '..\config\config.cfg'

class Partitions(object):
    '''
    Handles logical structure information of a device
    '''

    __devlist = None
    __mmls = None
    __config = None

    def __init__(self):
      '''
      Constructor
      '''
      try:
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_PATH)      
        self.__config = config
      except Exception as e:
        sys.stderr.write(repr(e) + " in config file.\n")
        traceback.print_exc()
  
    def init_menu(self):
      
      print('Choose a device:\n')
      self.__devlist = self.getDevices()
      
      #print(self.__devlist)
      
      i = 1
      for device in self.__devlist:
        print("%d . %s DevID: %s #partitions: %s" % (
            i, device['Model'], device['DeviceID'], device['Partitions']))
        i = i + 1
      # print (self.__menu_devs)
      
      ch = raw_input(" >>  ")
      self.exec_menu(ch)
    
    def getDevices(self):
      
#       # TODO put in config.cfg
#       cmd = ['powershell.exe',
#             'Get-WmiObject Win32_DiskDrive', '| format-list']

      cmd = ''.join([self.__config.get('commands', 'physicaldevice')])
      
      out = self.run_cmd(cmd)

      return self.parse_out(out)
      
    def parse_out(self, out):
      
      # split per device, quite fragile as a condition, but as long as PowerShell result is consistent we're ok
      out = re.split("\r\n\r\n", out)
      # filter empty elements
      disks = filter(None, out)

      tmp = []
      for disk in disks:  
        result={}
        for row in disk.split('\n'):
            if ': ' in row:
                key, value = row.split(': ')
                result[key.strip(' .')] = value.strip()
        tmp.append(result)

      return tmp
    
    def runMmls(self,ch):
      
      self.__mmls = Mmls()
      self.__mmls.set_dev_path(self.__devlist[int(ch)-1]['DeviceID'])
      self.__mmls.set_desc(str(self.__devlist[int(ch)-1]['Model']))
      self.__mmls.run()
    
    def exec_menu(self, ch):
        if ch == '':
            pass
        elif int(ch) == 0:
            return
        else:
            try:
                # run mmls tool against the specified device
                self.runMmls(ch)
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
