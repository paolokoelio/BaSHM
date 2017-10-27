'''
Created on 27 ott 2017

@author: koelio
'''

from pySMART import DeviceList, Device


class ChkHealth(object):
    '''
    Class for managing objects related to Disk Health through pySMART wrapper for smartmontools (https://www.smartmontools.org/)
    '''
    
    __devlist = None

    def __init__(self):
        '''
        Constructor
        '''
        
        self.__devlist = DeviceList()
        
    def chkhealth(self):
      
      print(self.__devlist)