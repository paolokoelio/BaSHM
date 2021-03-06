'''
Created on 20 nov 2017

@author: koelio
'''

import subprocess as sp
from utils.Timer import Timer

CONFIG_PATH = '..\config\config.cfg'


class L2t(object):
    '''
    Log2timeline super-timeline extraction
    '''
    
    __config = None
    __filename = None
    __offset = None
    __partitions = None # Partitions()
    __part_list = None
    __sel_dev = None # selected device
    __choice = None
    __param = False # optional fututre work parameter, not used

    def __init__(self, config, partitions):
        '''
        Constructor
        '''
        self.__partitions = partitions
        self.__config = config
        self.timer = Timer()

    def init_menu(self):
      # initialize menu
      print("Choose the disk from which to extract super-timeline\n")
      # Exploiting the menu listing feature from Partitions()
      self.__partitions.init_menu()
      self.__part_list = self.__partitions.runMmls()
      self.__sel_dev = self.__partitions.get_sel_dev()
      
      # ch = raw_input(" >>  ")
      # self.exec_menu(ch)
          
    def stimel(self):
      # launch command to start log2timeline for super-timeline extraction
      self.init_menu()
      
      model = str(self.__sel_dev['Model']).replace(' ', '')
      model = model.replace('USBDevice', '')
      directory = str('case_' + model)
      self.__filename = self.__config.get('paths', 'cases') + directory + '\\' + model + '_partition_' + str(self.__choice) + self.__config.get('plaso', 'output')

      device = self.__partitions.get_sel_dev()['DeviceID']
      
      cmd = ''.join([
        
            self.__config.get('paths', 'plaso'),
            self.__config.get('commands', 'l2t'),
            ' ',
            (' --parsers ' + self.__config.get('plaso', 'parsers_val')) if self.__config.getboolean('plaso', 'parsers') else '',
            ' ',
            self.__filename,
            ' -p' if self.__param else '',
            ' ' + device,
            ])

      self.timer.start()
      self.run_cmd(cmd)
      
      self.timer.stop()
      self.timer.printDuration()
      
      # now run convertion from storage.plaso file to .csv
      self.convertCsv(self.__filename, directory, model)

      return

    def convertCsv(self, filename, directory, model):
      # convert to CSV (method dup. TODO refactoring)
      print("Do you want to convert the storage.plaso file to .csv? Type y (or yes) to continue or abort with Enter\n")
      try: 
        ch = raw_input(" >>  ")
        
        if ch in ['yes', 'y']:
          cmd = ''.join([
                self.__config.get('paths', 'plaso'),
                self.__config.get('commands', 'psort'),
                ' -o l2tcsv',
                ' -w ' + self.__config.get('paths', 'cases') + directory + '\\' + model + '_supertimeline.csv',
                ' -p' if self.__param else '',
                ' ' + filename
                ])
    
          print("Starting conversion to .CSV: ")

          self.run_cmd(cmd)          

          self.convertHtml(directory, model)


        else: 
          print("A storage.plaso file has been created in " + directory + "\n")
          print("Use psort -o l2tcsv -w mac.csv storage.plaso to extract manually, psort -h for help.\n")
      except KeyboardInterrupt:
        print('Ended by user.')

    def convertHtml(self, directory, model):
        # convert to HTML (method dup. TODO refactoring)
        print("Do you want to generate an HTML report from the .CSV? Type y (or yes) to continue or abort with Enter\n")
        ch = raw_input(" >>  ")
        
        if ch in ['yes', 'y']:
          print("Please set the delta_t threshold in seconds, or press Enter for default of 60s.\n")
          min_t = raw_input(" >>  ")
          
          cmd = ''.join([
                self.__config.get('commands', 'python'),
                ' ',
                self.__config.get('paths', 'poggi'),
                self.__config.get('commands', 'lister'),
                (' -t ' +  min_t) if min_t != '' else '',
                ' -template ' + self.__config.get('paths', 'poggi') + self.__config.get('names', 'template'),
                ' -f ' + self.__config.get('paths', 'cases') + '\\' + directory + '\\' + model + "_supertimeline.csv"
                ' -o ' + self.__config.get('paths', 'cases') + '\\' + directory + '\\' + model + "_report_l2t.html"
                ])
    
          print("Started conversion to HTML: ")
          #print(cmd)
          self.run_cmd(cmd)
        else: 
          print("A .CSV file has been created in " + directory + "\n")
          print("Use python Lister.py to generate an HTML report manually, python Lister.py -h for help.\n")
      
    def run_cmd(self, cmd):
      '''
        Prints and runs specified command
      '''
      print('Issuing command: "' + cmd + '".')
      
      try:
          out = sp.check_call(cmd,
            # stdout=sp.STDOUT,
            stderr=sp.STDOUT,
            shell=True)
          print('\n')
          return out
      except sp.CalledProcessError as e:
          print("\nSomething went wrong. You may retry this action." + " ret_code: " + str(e.returncode) + "\n")
      except KeyboardInterrupt as k:
          print("\nAborted by user " + str(k) + "\n")
    
    def set_offset(self, value):
      self.__offset = value
    
    def exec_menu(self, ch):
      if ch == '':
          pass
      elif int(ch) == 0:
          return
      else:
          try:
              # set the offset of the corresponding partition
              self.__choice = ch
          except KeyError:
              print("Invalid selection, please try again.\n")
          except IndexError:
              print("Out of index, please choose frome the list again.\n")
              self.init_menu()
      return 

