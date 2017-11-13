'''
Created on 13 nov 2017

@author: koelio
'''

class Mmls(object):
    '''
    Gets partition layout of a volume; based on mmls module of TSK
    '''
    
    #Defaultvalues
    __dev_path = None
    __offset = 0
    __type = 'raw'
    __fstype = 'ntfs'

    def __init__(self):
        '''
        Constructor
        '''
    
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


    #TODO docum
    dev_path = property(get_dev_path, set_dev_path, del_dev_path, "dev_path's docstring")
    offset = property(get_offset, set_offset, del_offset, "offset's docstring")
    type = property(get_type, set_type, del_type, "type's docstring")
    fstype = property(get_fstype, set_fstype, del_fstype, "fstype's docstring")
        