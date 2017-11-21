'''
Created on 20 nov 2017

@author: koelio
'''

import subprocess as sp
# from bashm.menu import Menu

CONFIG_PATH = '..\config\config.cfg'

class TSKExtractor(object):
    '''
    Extracts timeline using standalone TSK 4.5
    '''

# usage: fls.exe [-adDFlhpruvV] [-f fstype] [-i imgtype] [-b dev_sector_size] [-m dir/] [-o imgoffset] [-z ZONE] [-s seconds] image [images] [inode]
#         If [inode] is not given, the root directory is used
#         -a: Display "." and ".." entries
#         -d: Display deleted entries only
#         -D: Display only directories
#         -F: Display only files
#         -l: Display long version (like ls -l)
#         -i imgtype: Format of image file (use '-i list' for supported types)
#         -b dev_sector_size: The size (in bytes) of the device sectors
#         -f fstype: File system type (use '-f list' for supported types)
#         -m: Display output in mactime input format with
#               dir/ as the actual mount point of the image
#         -h: Include MD5 checksum hash in mactime output
#         -o imgoffset: Offset into image file (in sectors)
#         -p: Display full path for each file
#         -r: Recurse on directory entries
#         -u: Display undeleted entries only
#         -v: verbose output to stderr
#         -V: Print version
#         -z: Time zone of original machine (i.e. EST5EDT or GMT) (only useful with -l)
#         -s seconds: Time skew of original machine (in seconds) (only useful with -l & -m)

    def __init__(self, config, partitions):
        '''
        Constructor
        '''
        self.__partitions = partitions
      
        self.__long_listing = False
        self.__recursive = False
        self.__print = False
        self.__hash = True
        self.__fout = None
        
        #Default args
        self.__image_type = 'raw'
        self.__fstype = 'ntfs'
        self.__images = None
        self.__offset = 0
        self.__inode = '/'
        self.__filename = None
        self.__device = None
             
        self.__config = config

          
    def init_menu(self):
      
      # Exploiting the menu listing feature from Partitions()
      self.__partitions.init_menu()
      self.__part_list = self.__partitions.get_part_list()
      self.__sel_dev = self.__partitions.get_sel_dev()
      
      ch = raw_input(" >>  ")
      self.exec_menu(ch)
    
    def TSKtimel(self):
      
      print("Launching TSK fls module..\n")
      self.init_menu()
      
      directory = str('case_' + str(self.__sel_dev['Model'])).replace(' ', '_')
      self.__filename = self.__config.get('paths','cases') + '\\' + directory + '\\' + "bodyTSK.txt"
      #print(self.__filename)
      self.__device = self.__partitions.get_sel_dev()['DeviceID']
      
      cmd = ''.join([
        
            self.__config.get('paths', 'tsk'),
            '\\',
            self.__config.get('commands', 'fls'),
            ' -r' if self.__recursive else '',
            ' -l' if self.__long_listing else '',
            ' -p' if self.__print else '',
            ' -h' if self.__hash else '',
            ' -f ' + self.__fstype,
            ' -i ' + self.__image_type,
            ' -m "/" ',
            '-o ',
            str(self.__offset/512),
            ' ' + self.__device,
#             ' ' + self.__inode, makes TSK crash
            ' > ',
            self.__filename
            ])

      #print(cmd)
      self.run_cmd(cmd)
      
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
    
    def setOff(self, ch):
      
      # where offset in block is
      off_index = 3
      #print('{}'.format(self.__part_list[int(ch)]))
      self.__offset = int(self.__part_list[int(ch)][off_index])
    
    def exec_menu(self, ch):
      if ch == '':
          pass
      elif int(ch) == 0:
          return
      else:
          try:
              # set the offset of the corresponding partition
              self.setOff(ch)
          except KeyError:
              print("Invalid selection, please try again.\n")
              pass
      return 
      
    