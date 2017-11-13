'''
Created on 11 nov 2017

@author: koelio
'''
import os

permissionDict ={
  'access':{
    '0':('---'),
    '1':('--x'),
    '2':('-w-'),
    '3':('-wx'),
    '4':('r--'),
    '5':('r-x'),
    '6':('rw-'),
    '7':('rwx')
  },

  'roles':{
    0:'owner',
    1:'group',
    2:'other'
  }  
}

from stat import (S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IWGRP,
                  S_IXGRP, S_IROTH, S_IWOTH, S_IXOTH)

def bit2int(bit):
    return int(oct(bit))

def convert_st_mode(st_mode):
    bits = (S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IWGRP, S_IXGRP,
            S_IROTH, S_IWOTH, S_IXOTH)
    mode = "%03d" % sum(int(bool(st_mode & bit)) * bit2int(bit) for bit in bits)
    return mode

def get_unix_permissions(pth):
    mode = convert_st_mode(os.stat(pth).st_mode)
    return mode
  
def convert_to_symbolic(mode):
  permissionOctal = oct(int(mode))[1:4] #we have to remove the L: int mode = [365L]
  #print(int(mode), permissionOctal) #debug
  out = [] #645
  for role,octal in enumerate(permissionOctal): # [(0,6) , (1,4) , (2,5)], role is needed because octal is a tuple
    out.append(permissionDict['access'][octal])
#   print(''.join(out))
  return out
    