'''
Created on 10 nov 2017

@author: koelio
'''

import subprocess as sp
from Fls import Fls


class Extractor(object):
    '''
    classdocs
    '''
    __fls = None
    __l2t = None
    __devlist = None
    __config = None
    __partitions = None
    __mmls = None
    __part_list = None  # partition list of the selected device in Partition during menu choice
    __sel_dev = None  # device selected in Partition class during menu choice
    __offset = None
    __suffix = '_body.txt'
    __choice = None

    def __init__(self, config, partitions):
      '''
      Constructor
      '''
      self.__partitions = partitions
      self.__config = config
      self.__fls = Fls()
      
    def init_menu(self):
      
      # Exploiting the menu listing feature from Partitions()
      self.__partitions.init_menu()
      self.__part_list = self.__partitions.runMmls()
      
      #self.__part_list = self.__partitions.get_part_list()
      self.__sel_dev = self.__partitions.get_sel_dev()
      
      ch = raw_input(" >>  ")
      self.exec_menu(ch)
    
    def timel(self):
      '''
      Perform timeline extraction
      '''
      print("Launching fls module..\n")
      self.init_menu()
      
      self.__fls.set_offset(self.__offset)
      
      # set pathname for extracting the timeline
      model = str(self.__sel_dev['Model']).replace(' ', '')
      model = model.replace('USBDevice', '')
      directory = str('case_' + model)
      filename = self.__config.get('paths', 'cases') + '\\' + directory + '\\' + model + '_partition_'+ str(self.__choice) + self.__suffix
      self.__fls.set_filename(filename)
      self.__fls.set_recursive(self.__config.getboolean('functionalities', 'recursive'))
      
      # set the physical device
      self.__fls.set_images([self.__partitions.get_sel_dev()['DeviceID']])
      
      # we leave the rest default, and launch fls (TODO: set timer)
      if self.__fls.extractTimel() == 0:
        print("Success! Written to {} ".format(filename))
        
        self.convertCsv(filename, directory, model)
        
      else:
        print("Uh-oh")

      return
    
    def convertCsv(self, filename, directory, model):    # now run convertion
      print("Do you want to convert the body.txt file to .csv? Type y (or yes) to continue or abort with Enter\n")
      
      try:
        ch = raw_input(" >>  ")
        
        if ch in ['yes', 'y']:
          cmd = ''.join([
                self.__config.get('commands', 'perl'),
                ' ',
                self.__config.get('paths', 'tsk') + '\\' + 'mactime.pl',
                ' ',

                ' -d',
                ' -b ' + filename,
                ' > ' + self.__config.get('paths', 'cases') + '\\' + directory + '\\' + model + '_partition_' + self.__choice + "_timeline.csv"
                ])
    
          print("Started conversion to .CSV: ")
          self.run_cmd(cmd)
          
          self.convertHtml(directory, model)
          
        else: 
          print("A body.txt file has been created in " + directory + "\n")
          print("Use perl mactime.pl -d -b body.txt to extract the CSV manually, perl mactime.pl -h for help.\n")
      except KeyboardInterrupt:
        print('Ended by user.')
    
    def convertHtml(self, directory, model):
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
                ' -f ' + self.__config.get('paths', 'cases') + '\\' + directory + '\\' + model + '_partition_' + self.__choice + "_timeline.csv"
                ' -o ' + self.__config.get('paths', 'cases') + '\\' + directory + '\\' + model + '_partition_' + self.__choice + "_report.html"
                ])
    
          print("Started conversion to HTML: ")
          #print(cmd)
          self.run_cmd(cmd)
        else: 
          print("A .CSV file has been created in " + directory + "\n")
          print("Use python Lister.py to generate an HTML report manually, python Lister.py -h for help.\n")
    
    def browse(self):
      '''
      Browse the FS on the image
      '''
      print("This function is left for future work.")
      return
    
    def setOff(self, ch):
      # where offset in block is in the partition list
      off_index = 3
      self.__offset = int(self.__part_list[int(ch)][off_index])
    
    def exec_menu(self, ch):
      if ch == '':
          pass
      elif int(ch) == 0:
          return
      else:
          try:
              # set the offset of the corresponding partition
              self.__choice = ch
              self.setOff(ch)
          except KeyError:
              print("Invalid selection, please try again.\n")
              pass
      return 
  
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
          return -2
      
