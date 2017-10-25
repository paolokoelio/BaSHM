'''
Created on 24 ott 2017

@author: koelio
'''

import subprocess as sp
# from bashm.menu import Menu

class Chkmnt(object):
    '''
    Checks if the AUTOMOUNT is turned off and can de/activate it.
    '''

    __config = None

    def __init__(self, config):
        '''
        Constructor
        '''
#         try:
        self.__config = config
#         except Exception, e:
#           sys.stderr.write(repr(e) + " in config file.\n")
          #traceback.print_exc()
        
        #yolo
    def check(self):
      
      #out = sp.check_output(['diskpart','/s','\win_scripts\chkmnt.txt'])
      print('Issuing command: "' + self.__config.get('commands', 'diskpart')
            + self.__config.get('paths', 'static')
            + self.__config.get('names', 'chkmnt') +'"')
      
      out = sp.call(self.__config.get('commands', 'diskpart') + " "
            + self.__config.get('paths', 'static')
            + self.__config.get('names', 'chkmnt'),
             shell=True)
      
      print(out)
      self.back_to_menu()
      
#     def back_to_menu(self):
#       menu = Menu(self.__config)
#       menu.main_menu()
      