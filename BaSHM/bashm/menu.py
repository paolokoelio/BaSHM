'''
Created on 23 ott 2017

@author: koelio
'''
import subprocess as sp
import sys, traceback
from chkmnt.Chkmnt import Chkmnt
from diskinfo.DiskInfo import DiskInfo
from partitions.Partitions import Partitions
from extractor.Extractor import Extractor
from extractor.TSKExtractor import TSKExtractor
from extractor.L2t import L2t


class Menu(object):
  '''
  Main menu for choosing actions.
  '''
  # some declarations
  __config = None
  __checkMount = None
  __checkHealth = None
  __extractor = None
  __TSKextractor = None
  __partitions = None
  __Lt2 = None
  
  # Main definition
  __menu_actions = {}
  
  mainMenuLabels = ["Please choose the action you want to launch:",
                           "1. Check and Deactivate AUTOMOUNT",
                           "2. Device information and SMART data",
                           "3. Get logical structure of a device",
                           "4. Extract Time-lines",
                           "\n0. Quit"]
  
  checkMountLabels = ["Before connecting the Disk disable Windows AUTOMOUNT:",
                              "1. Check AUTOMOUNT",
                              "2. Disable AUTOMOUNT",
                              "3. Enable AUTOMOUNT",
                              "9. Back",
                              "0. Quit"
                              ]
  checkHealthLabels = ["Perform SMART Health Test:",  # TODO add disk info entry
                              "1. SMART Health test with smartmontools",
                              "2. Open dd shell (future work)",
                              "9. Back",
                              "0. Quit"
                              ]
  
  partitionsLabels = ["Get device logical structure",
                      "1. Get partitioning information",
                      "2. Open mmls shell (future work)",
                      "9. Back",
                      "0. Quit"
    
    ]
  
  extractorLabels = ["Choose the artifacts to TSKtimel:",
                              "1. Timeline TSK 4.5",
                              "2. Super-timeline (log2timeline)",
                              "3. Timeline with custom TSK library (experimental)",
                              "4. Browse only (future work)",
                              "9. Back",
                              "0. Quit"
                              ]

  def __init__(self, config):
    
    '''
    Menu entries definitions and initialize Classes
    '''
    
    self.__config = config
    
    self.__partitions = Partitions(self.__config)
    self.__checkMount = Chkmnt(self.__config)
    self.__checkHealth = DiskInfo(self.__partitions)
    self.__extractor = Extractor(self.__config, self.__partitions)
    self.__TSKextractor = TSKExtractor(self.__config, self.__partitions)
    self.__L2t = L2t(self.__config, self.__partitions)
    
    # dictionaries that map menu choices to relative methods
    self.__chkmnt_menu = {
        '1':self.__checkMount.check,
        '2':self.__checkMount.deactmnt,
        '3':self.__checkMount.actmnt,
        '9':self.back,
        '0':self.exit,
    }
    
    self.__chkHealth_menu = {
        '1':self.__checkHealth.init_menu,
        '2':self.__checkHealth.openDD,  # TODO
        '9':self.back,
        '0':self.exit,
    }
    
    self.__extractor_menu = {
        '1':self.__TSKextractor.TSKtimel,
        '2':self.__L2t.stimel,
        '3':self.__extractor.timel,
        '4':self.__extractor.browse,
        '9':self.back,
        '0':self.exit,
    }
    
    self.__partitions_menu = {
        '1':self.__partitions.getPartInfo,
        '2':self.__partitions.openShell,
        '9':self.back,
        '0':self.exit,
    }

    # Main menu definition
    self.__menu_actions = {
        'main_menu': self.main_menu,
        '1': self.chkmnt,
        '2': self.health,
        '3': self.partitions,
        '4': self.TSKtimel,
        'chkmnt': self.__chkmnt_menu,
        'diskinfo': self.__chkHealth_menu,
        'partitions': self.__partitions_menu,
        'TSKtimel': self.__extractor_menu,
        '9': self.back,
        '0': self.exit,
    }

  # =======================
  #     MENUS FUNCTIONS
  # =======================
   
  # Main menu
  def main_menu(self):
      for m in self.mainMenuLabels:
        print(m)
      choice = raw_input(" >>  ")
      ch = [choice.lower()]
      self.exec_menu(ch)
   
      return
  
  # Execute menu
  def exec_menu(self, ch):
      cls()
      if ch[0] == '':
          self.__menu_actions['main_menu']()
      else:
          try:
              # execute selected action  
              self.get_in_dic(ch)
          except KeyError:
              print("Invalid selection, please try again.\n")
              self.__menu_actions['main_menu']()
      return
  
  # Util to call a method up to 2nd depth level
  def get_in_dic(self, ch):
    mn = self.__menu_actions
    if ch[0] in mn:
      # if this is a second level menu
      if len(ch) > 1:
        if ch[1] in mn[ch[0]]:
          # then go to second level choice
          mn[ch[0]][ch[1]]()
      else:
        # else go to first level choice
        mn[ch[0]]()
    # get back to main menu by default
    mn['main_menu']()
    return
   
  # Menu for check AUTOMOUNT (TODO refactoring method duplication, see below)
  def chkmnt(self):
      for m in self.checkMountLabels:
        print(m)
      choice = raw_input(" >>  ")
      choice = ['chkmnt' , choice.lower()]
      self.exec_menu(choice)
      return
   
  # Menu for Health check with SMART
  def health(self):
      for m in self.checkHealthLabels:
        print(m)
      choice = raw_input(" >>  ")
      choice = ['diskinfo' , choice.lower()]
      self.exec_menu(choice)
      return

  # Menu for logical disk structure
  def partitions(self):
      cls()
      for m in self.partitionsLabels:
        print(m)
      choice = raw_input(" >>  ")
      choice = ['partitions' , choice.lower()]
      self.exec_menu(choice)
      return
    
  # Menu for extracting timelines (END TODO refactoring)
  def TSKtimel(self):
      for m in self.extractorLabels:
        print(m)
      choice = raw_input(" >>  ")
      choice = ['TSKtimel' , choice.lower()]
      self.exec_menu(choice)
      return
   
  # Back to main menu
  def back(self):
      self.__menu_actions['main_menu']()
   
  # Exit program
  def exit(self):
      sys.exit(0)
      return    
    
def cls():
    sp.call('cls', shell=True)
