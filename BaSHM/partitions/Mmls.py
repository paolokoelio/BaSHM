'''
Created on 13 nov 2017

@author: koelio
'''

from examples import images
import pytsk3


class Mmls(object):
    '''
    Gets partition layout of a volume; based on mmls module of TSK
    '''
    
    # Default values
    __dev_path = None
    __offset = 0
    __type = 'raw'
    __fstype = 'ntfs'
    __block_size = 512  # KB, assumed default block size
    __desc = None
    __part_list = []
    __factor = 1024 * 1024

    def __init__(self):
        '''
        Constructor
        '''
    
    def mmls(self):
      
      img = images.SelectImage(self.__type, [self.__dev_path])
      
      try:
        volume = pytsk3.Volume_Info(img)
        
#         list =[]
#         entries = {'addr':[],
#                  'desc':[], 'start':[], 'start512':[], 'len':[]}
#           list.append(entry)

        for part in volume:

#           entry = {'addr':part.addr, 'desc':part.desc, 'start':int(part.start), 'start512':int(part.start * 512), 'len':int(part.len)}
#           list.append(entry)
          self.__part_list.append([part.addr, part.desc,part.start,part.start * self.__block_size,part.len,part.len * self.__block_size / (self.__factor)])
        
        print('Partition structure for: ' + self.__desc + '\n')
        print('{0:<2} {1:<30}\t{2:>15} {3:>15}\t{4:>15}\t{5:>7}'.format('#', 'Desc', 'Start sector', 'Start block', 'Length', 'Size'))
        
        for part in self.__part_list:
          print('{:<2} {:<30}\t{:>15} {:>15}\t{:>15}\t{:>7} MB'.format(part[0],part[1],part[2],part[3],part[4],part[5]))
#               )
#         # print(part.addr, part.desc, "%ss(%s)" % (int(part.start), int(part.start * 512)), int(part.len)) #example alternative
#       print('\n')
          
#           print('{:<2} {:<30}\t{:>15} {:>15}\t{:>15}\t{:>7} MB'.format(part.addr,
#                                                                   part.desc,
#                                                                   part.start,
#                                                                   part.start * self.__block_size,
#                                                                   part.len,
#                                                                   part.len * self.__block_size / (1024 * 1024),
#                                                                   )
#                 )
          # print(part.addr, part.desc, "%ss(%s)" % (int(part.start), int(part.start * 512)), int(part.len)) #example alternative
        print('\n')
#         print(self.__part_list)
              
      except IOError as e:
        print ("Error %s: Maybe specify a different image type "
                % e)
      
      return self.__part_list
    
    def set_all_params(self, path, offset, itype, fstype):
      self.__dev_path = path
      self.__offset = offset
      self.__type = itype
      self.__fstype = fstype
    
    def get_dev_path(self):
      return self.__dev_path

    def get_offset(self):
      return self.__offset

    def get_type(self):
      return self.__type

    def get_fstype(self):
      return self.__fstype

    def set_dev_path(self, value):
      self.__dev_path = value

    def set_offset(self, value):
      self.__offset = value

    def set_type(self, value):
      self.__type = value

    def set_fstype(self, value):
      self.__fstype = value

    def del_dev_path(self):
      del self.__dev_path

    def del_offset(self):
      del self.__offset

    def del_type(self):
      del self.__type

    def del_fstype(self):
      del self.__fstype

    def get_block_size(self):
      return self.__block_size

    def get_desc(self):
      return self.__desc

    def set_block_size(self, value):
      self.__block_size = value

    def set_desc(self, value):
      self.__desc = value

    def del_block_size(self):
      del self.__block_size

    def del_desc(self):
      del self.__desc

        
