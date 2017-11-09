'''
Created on 24 ott 2017

@author: koelio
'''

import subprocess as sp
import ConfigParser
# from bashm.menu import Menu


CONFIG_PATH = '..\config\config.cfg'

class Chkmnt(object):
    '''
    Checks if the AUTOMOUNT is turned on and can dis/enable it.
    '''

    __config = None

    def __init__(self):
      '''
      Constructor
      '''
          #try:
      config = ConfigParser.ConfigParser()
      config.read(CONFIG_PATH)
#         
      self.__config = config
#         except Exception, e:
#           sys.stderr.write(repr(e) + " in config file.\n")
          #traceback.print_exc()
        
        #yolo
    def check(self):
      
      #out = sp.check_output(['diskpart','/s','\win_scripts\chkmnt.txt'])
      print('Issuing command: "' + self.__config.get('commands', 'diskpart')
            + self.__config.get('paths', 'static')
            + self.__config.get('names', 'chkmnt') +'"' )
      print('Needs to be run as Priviledged User')
      
      try:
          sp.check_output(self.__config.get('commands', 'diskpart') + " "
            + self.__config.get('paths', 'static')
            + self.__config.get('names', 'chkmnt'),
             stderr=sp.STDOUT,
             shell=True)
      except sp.CalledProcessError:
          print("Something went wrong. You may retry this action." + " ret_code: " + str(sp.returncode) + "\n")
      
      return
      
    #TODO exception handling
    def deactmnt(self): 
      print('Issuing command: "' + self.__config.get('commands', 'deactmnt'))
      print('needs to be run as Priviledged User')
  
      out = sp.call(self.__config.get('commands', 'deactmnt'),
             shell=True)
      
      print(out)
      if out == 0:
        print('AUTOMOUNT disabled successfully')
        print('Now you can connect the Disk')
      
      return

    #TODO exception handling
    def actmnt(self):
      print('Issuing command: "' + self.__config.get('commands', 'actmnt'))
      print('needs to be run as Priviledged User')
  
      out = sp.call(self.__config.get('commands', 'actmnt'),
             shell=True)
      
      print(out)
      return
      