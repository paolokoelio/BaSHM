'''
Created on 24 ott 2017

@author: koelio
'''

import subprocess as sp


class Chkmnt(object):
    '''
    Checks if the AUTOMOUNT is turned on and can dis/enable it.
    '''

    __config = None

    def __init__(self, config):
      '''
      Constructor
      '''
      self.__config = config
           
    def check(self):
      cmd = ''.join([self.__config.get('commands', 'diskpart'),
            ' ',
            self.__config.get('paths', 'static'),
            self.__config.get('names', 'chkmnt')])

      self.run_cmd(cmd)
      
    def deactmnt(self): 
      cmd = self.__config.get('commands', 'deactmnt')
      
      out = self.run_cmd(cmd)
      if out == 0:
        print('AUTOMOUNT disabled successfully.\nYou you can now connect the Disk safely.\n')

    def actmnt(self):
      cmd = self.__config.get('commands', 'actmnt')
      if self.run_cmd(cmd) == 0:
        print('AUTOMUNT enabled successfully.\n')
      
    def run_cmd(self, cmd):
      '''
        Prints and runs specified command
      '''
      print('Needs to be run as Privileged User.')
      print('Issuing command: "' + cmd + '".')
      
      try:
          out = sp.check_call(cmd,
            # stdout=sp.STDOUT,
            stderr=sp.STDOUT,
            shell=True)
          print('\n')
      except sp.CalledProcessError as e:
          print("\nSomething went wrong. You may retry this action." + " ret_code: " + str(e.returncode) + "\n")
      
      return out
