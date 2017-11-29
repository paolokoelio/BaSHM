'''
Created on 10 nov 2017

Class responsible for iterating through the selected image and construct a timeline of all data contained in the $MFT

@author: koelio
'''
#!/usr/bin/python
#
# Copyright 2011, Michael Cohen <scudette@gmail.com>.
#     http://www.apache.org/licenses/LICENSE-2.0

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import argparse
# import gc
# import pdb
import sys


from examples import images
import pytsk3

from utils.mode_convert import convert_to_symbolic


class Fls(object):

  FILE_TYPE_LOOKUP = {
      pytsk3.TSK_FS_NAME_TYPE_UNDEF: "-",
      pytsk3.TSK_FS_NAME_TYPE_FIFO: "p",
      pytsk3.TSK_FS_NAME_TYPE_CHR: "c",
      pytsk3.TSK_FS_NAME_TYPE_DIR: "d",
      pytsk3.TSK_FS_NAME_TYPE_BLK: "b",
      pytsk3.TSK_FS_NAME_TYPE_REG: "r",
      pytsk3.TSK_FS_NAME_TYPE_LNK: "l",
      pytsk3.TSK_FS_NAME_TYPE_SOCK: "h",
      pytsk3.TSK_FS_NAME_TYPE_SHAD: "s",
      pytsk3.TSK_FS_NAME_TYPE_WHT: "w",
      pytsk3.TSK_FS_NAME_TYPE_VIRT: "v"}

  META_TYPE_LOOKUP = {
      pytsk3.TSK_FS_META_TYPE_REG: "r",
      pytsk3.TSK_FS_META_TYPE_DIR: "d",
      pytsk3.TSK_FS_META_TYPE_FIFO: "p",
      pytsk3.TSK_FS_META_TYPE_CHR: "c",
      pytsk3.TSK_FS_META_TYPE_BLK: "b",
      pytsk3.TSK_FS_META_TYPE_LNK: "h",
      pytsk3.TSK_FS_META_TYPE_SHAD: "s",
      pytsk3.TSK_FS_META_TYPE_SOCK: "s",
      pytsk3.TSK_FS_META_TYPE_WHT: "w",
      pytsk3.TSK_FS_META_TYPE_VIRT: "v"}

  ATTRIBUTE_TYPES_TO_PRINT = [
      pytsk3.TSK_FS_ATTR_TYPE_NTFS_IDXROOT,
      pytsk3.TSK_FS_ATTR_TYPE_NTFS_DATA,
      pytsk3.TSK_FS_ATTR_TYPE_DEFAULT]

  def __init__(self):
    super(Fls, self).__init__()
    self._fs_info = None
    self._img_info = None
    self._long_listing = True
    self._recursive = False
    self._print = False
    self._fout = None
    
    #Default args
    self.__image_type = 'raw'
    self.__images = None
    self.__offset = 0
    self.__inode = '/'
    #self.__print = False
    #self.__recursive = True
    self.__filename = None

#   def filemode(self, m):
#       '''
#       Mode m to be converted
#       '''
#       oExec = bool(m & 0001)
#       oWrite = bool(m & 0002)
#       oRead = bool(m & 0004)
#       gExec = bool(m & 0010)
#       gWrite = bool(m & 0020)
#       gRead = bool(m & 0040)
#       otExec = bool(m & 0100)
#       otWrite = bool(m & 0200)
#       otRead = bool(m & 0400)
#       
#       modes = {oExec:'e',
#                oWrite:'w',
#                oRead:'r',
#                gExec:'e',
#                gWrite:'w',
#                gRead:'r',
#                otExec: 'e',
#                otWrite: 'w',
#                otRead: 'r',
#                }
#       
#       return str()

  def list_directory(self, directory, stack=None):
    stack.append(directory.info.fs_file.meta.addr)

    for directory_entry in directory:
      prefix = "+" * (len(stack) - 1)
      if prefix:
        prefix += " "

      # Skip ".", ".." or directory entries without a name.
      if (not hasattr(directory_entry, "info") or
          not hasattr(directory_entry.info, "name") or
          not hasattr(directory_entry.info.name, "name") or
          directory_entry.info.name.name in [".", ".."]):
        continue

      self.print_directory_entry(directory_entry, prefix=prefix)

      if self._recursive:
        try:
          sub_directory = directory_entry.as_directory()
          inode = directory_entry.info.meta.addr

          # This ensures that we don't recurse into a directory
          # above the current level and thus avoid circular loops.
          if inode not in stack:
            self.list_directory(sub_directory, stack)

        except IOError:
          pass

    stack.pop(-1)

  def open_directory(self, inode_or_path):
    inode = None
    path = None
    if inode_or_path is None:
      path = "/"
    elif inode_or_path.startswith("/"):
      path = inode_or_path
    else:
      inode = inode_or_path

    # Note that we cannot pass inode=None to fs_info.opendir().
    if inode:
      directory = self._fs_info.open_dir(inode=inode)
    else:
      directory = self._fs_info.open_dir(path=path)

    return directory

  def open_file_system(self, offset):
    self._fs_info = pytsk3.FS_Info(self._img_info, offset=offset)

  def open_image(self, image_type, filenames):
    # List the actual files (any of these can raise for any reason).
    self._img_info = images.SelectImage(image_type, filenames)

  def open_fout(self, filename):
    # Outputs to a UTF-8 .txt file
    
    try:
      if not self._print:
        self._fout = open(filename, 'wb')
    
    except IOError as io:
      #traceback.print_exc()
      print("Consider creating a case directory first in menu 2.\n{} \n".format(io))    
      return 2
        
  def close_fout(self):
    if not self._print:
      self._fout.close()

  def parse_options(self, options):
    self._long_listing = getattr(options, "long_listing", False)
    self._recursive = getattr(options, "recursive", False)
    self._print = getattr(options, "print", False)

  def print_directory_entry(self, directory_entry, prefix=""):
      meta = directory_entry.info.meta
      name = directory_entry.info.name

      name_type = "-"
      if name:
        name_type = self.FILE_TYPE_LOOKUP.get(int(name.type), "-")

      meta_type = "-"
      if meta:
        meta_type = self.META_TYPE_LOOKUP.get(int(meta.type), "-")

      directory_entry_type = "{0:s}/{1:s}".format(name_type, meta_type)

      for attribute in directory_entry:
        inode_type = int(attribute.info.type)
        if inode_type in self.ATTRIBUTE_TYPES_TO_PRINT:
          if self._fs_info.info.ftype in [
              pytsk3.TSK_FS_TYPE_NTFS, pytsk3.TSK_FS_TYPE_NTFS_DETECT]:
            inode = "{0:d}-{1:d}-{2:d}".format(
                meta.addr, int(attribute.info.type), attribute.info.id)
          else:
            inode = "{0:d}".format(meta.addr)

          attribute_name = attribute.info.name
          if attribute_name and attribute_name not in ["$Data", "$I30"]:
            filename = "{0}:{1}".format(name.name.decode("utf-8"), attribute.info.name.decode("utf-8"))
          else:
            filename = name.name.decode("utf-8")

#           times = [meta.crtime, meta.ctime, meta.mtime, meta.atime] #probably wron disposition
          times = [meta.atime, meta.mtime, meta.ctime, meta.crtime]


#           choppiamo il primo char perche' viene '?'
#           no filemode attribute for python2.7, thus custom method         
#           mode = self.filemode(meta.mode)[1:]
          mode = convert_to_symbolic(meta.mode)

          permissions = "{0}{1}".format(directory_entry_type, ''.join(mode))

          md5 = 0  # TODO

          if meta and name:
            out = "{0}|{1}|{2}|{3}|{4:d}|{5:d}|{6:d}|{7:d}|{8:d}|{9:d}|{10:d}".format(
                  md5, filename, inode, permissions, meta.uid, meta.gid, meta.size,
                  int(times[0]), int(times[1]), int(times[2]), int(times[3]))

            if self._print:
              print(out)
            else:
              self._fout.write("{}\n".format(out).encode("utf-8"))
            
  def extractTimel(self):
    
    print("Extracting timeline to: {}\n".format(self.__filename))
    print("Performing equivalent TSK command to: fls -f ntfs -i {} -o {} {} {}\n".format(self.__image_type, self.__offset, ''.join(self.__images), self.__inode))
    
    # VOL = ['\\\?\Volume{9eeddfb1-0000-0000-0000-505e3a000000}']
    # self._images = ['\\\.\PHYSICALDRIVE1']
    # VOL = ['\\\?\Volume{52c225e9-0000-0000-0000-50f90d000000}']
    # VOL = ['D:\FTK\win10_C.001']
    
    # image_type='raw', images=['yo'], images=['yo'], offset=0, print=False, recursive=False
    options = {'image_type':self.__image_type,
               'images':self.__images,
               'offset':self.__offset,
               'inode':self.__inode,
               'print':self._print,
               'recursive':self._recursive,
               'filename':self.__filename,
               }
    
    self.open_image(options['image_type'], options['images'])
  
    try:
      try:
        #filename = '../files_tmp/body.txt'
        
        self.open_fout(self.__filename)
      
        self.open_file_system(options['offset'])
  
        directory = self.open_directory(options['inode'])
      
        # Iterate over all files in the directory and print their name.
        # What you get in each iteration is a proxy object for the TSK_FS_FILE
        # struct - you can further dereference this struct into a TSK_FS_NAME
        # and TSK_FS_META structs.
        self.list_directory(directory, [])
      
        self.close_fout()
      
      except IOError as io:
        #traceback.print_exc()
        print("Consider creating a case directory first in menu 2.\n{} \n".format(io))    
        return 2
    
    except Exception as e:
      print("Generic error occurred: \n{}".format(e))
      return 2
    
    return 0

  def get_recursive(self):
    return self.__recursive


  def get_image_type(self):
    return self.__image_type


  def get_images(self):
    return self.__images


  def get_offset(self):
    return self.__offset


  def get_inode(self):
    return self.__inode


  def set_recursive(self, value):
    self.__recursive = value


  def set_image_type(self, value):
    self.__image_type = value


  def set_images(self, value):
    self.__images = value


  def set_offset(self, value):
    self.__offset = value


  def set_inode(self, value):
    self.__inode = value
  
  def set_filename(self, value):
    self.__filename = value


#Taken from examples, can launch fls as a commandline tool
def Main():
  """The main program function.

  Returns:
    A boolean containing True if successful or False if not.
  """
  args_parser = argparse.ArgumentParser(description=(
      "Lists a file system in a storage media image or device."))

  args_parser.add_argument(
      "images", nargs="+", metavar="IMAGE", action="store", type=str,
      default=None, help=("Storage media images or devices."))

  args_parser.add_argument(
      "inode", nargs="?", metavar="INODE", action="store",
      type=str, default=None, help=(
          "The inode or path to list. If [inode] is not given, the root "
          "directory is used"))

  # TODO: not implemented.
  # args_parser.add_argument(
  #     "-f", "--fstype", metavar="TYPE", dest="file_system_type",
  #     action="store", type=str, default=None, help=(
  #         "The file system type (use \"-f list\" for supported types)"))

  args_parser.add_argument(
      "-i", "--imgtype", metavar="TYPE", dest="image_type", type=str,
      choices=["ewf", "qcow", "raw"], default="raw", help=(
          "Set the storage media image type."))

  # TODO: not implemented.
  # args_parser.add_argument(
  #     "-l", dest="long_listing", action="store_true", default=False,
  #     help="Display long version (like ls -l)")

  args_parser.add_argument(
      "-o", "--offset", metavar="OFFSET", dest="offset", action="store",
      type=int, default=0, help="The offset into image file (in bytes)")

  args_parser.add_argument(
      "-r", "--recursive", dest="recursive", action="store_true",
      default=False, help="List subdirectories recursively.")
  
  args_parser.add_argument(
      "-p", "--print", dest="print", action="store_true",
      default=False, help="Print output to stdout.")

  args_parser.add_argument(
    "--file", nargs="+", metavar="FILENAME", dest="filename", action="store", type=str,
    default='body.txt', help=("Where to write output."))

  options = args_parser.parse_args()

  if not options.images:
    print('No storage media image or device was provided.')
    print('')
    args_parser.print_help()
    print('')
    return False

  print(options)
  #return True
  
  fls = Fls()
  fls.parse_options(options)
  
  fls.open_image(options.image_type, options.images)

  fls.open_fout(options.filename[0])

  fls.open_file_system(options.offset)

  directory = fls.open_directory(options.inode)

  fls.list_directory(directory, [])

  fls.close_fout()

  return True

if __name__ == '__main__':
  if not Main():
    sys.exit(1)
  else:
    sys.exit(0)
