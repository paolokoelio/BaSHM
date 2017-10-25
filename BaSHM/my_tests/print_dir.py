'''
Created on Jul 8, 2017
A test to open an image, its file system and list directories.
@author: koelio
'''
import sys
import pytsk3
#from examples import fls

def Main():

  #fls1 = fls.Fls()

  #fls1.open_image("raw", ['D:\\FTK\\win10_C.001'])
#   image = pytsk3.Img_Info('D:\FTK\win10_C.001')
  VOLUME_PATH = r'\\?\Volume{9eeddfb1-0000-0000-0000-505e3a000000}'
#   VOLUME_PATH = 'D:\FTK\win10_C.001'
  print(VOLUME_PATH)


  image = pytsk3.Img_Info(VOLUME_PATH)
  

  '''oggetto di pytsk3.Img_Info'''
  #fls1._img_info

  #fls1.open_file_system(0)
  fs_info = pytsk3.FS_Info(image, 0)
  
  '''oggetto di pytsk3.FS_Info'''
  #fls1._fs_info
  
  "Path della directory to be listed"
  directory = fs_info.open_dir('/')
  
  
  print("{0:s} \t {1:s}".format("inode","name"))
  for dir_entry in directory:
    meta = dir_entry.info.meta
    name = dir_entry.info.name
    
    # docs at http://www.sleuthkit.org/sleuthkit/docs/api-docs/4.3/structTSK__FS__NAME.html#details
    
    
    
#     if meta.addr == 0: 
    print("{0:d} \t {1:s}".format(meta.addr,name.name))
    #print("file_entry info:")
    print("\t {0:s} \t {1:>33}".format("type", "id"))
    for attr in fs_info.open_meta(meta.addr):
      print("\t {0:<30} \t {1:d}".format(attr.info.type, attr.info.id))
#       print("\t {0:<30}".format(attr.info))
          #length of blocks occupied by a file
#         for run in attr:
#             print "   Blocks %s to %s (%s blocks)" % (run.addr, run.addr + run.len, run.len)
    else:
      pass
      #print("{0:d} \t {1:s}".format(meta.addr,name.name))
    #print(meta +" " + name)
    #print("\n")

    
  pass

if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)