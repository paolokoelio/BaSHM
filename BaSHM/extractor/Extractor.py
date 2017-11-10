'''
Created on 10 nov 2017

@author: koelio
'''

from utils.ConcereteWriter import ConcreteWriter
from Fls import Fls


class Extractor(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def timel(self):
      '''
      Perform timeline extraction
      '''
      fls = Fls()
      fls.parse_options(options)
    
    #   fls.open_image(options.image_type, options.images)
    
      VOL = ['\\\?\Volume{9eeddfb1-0000-0000-0000-505e3a000000}']
      # VOL = ['D:\FTK\win10_C.001']
      fls.open_image(options.image_type, VOL)
    
      filename = 'body.txt'
    
      fls.open_fout(filename)
    
      fls.open_file_system(options.offset)
    
      directory = fls.open_directory(options.inode)
    
      # Iterate over all files in the directory and print their name.
      # What you get in each iteration is a proxy object for the TSK_FS_FILE
      # struct - you can further dereference this struct into a TSK_FS_NAME
      # and TSK_FS_META structs.
      fls.list_directory(directory, [])
    
      fls.close_fout()
    
      return True
    
    def stimel(self):
      '''
      Perform super-timeline extraction
      '''
      
      
      return
    
    def browse(self):
      '''
      Browse the FS on the image
      '''
      print("This function is left for future work.")
      return