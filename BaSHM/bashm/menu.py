'''
Created on 23 ott 2017

@author: koelio
'''
import subprocess as sp  # for screen cleaning (cls)
import sys
from chkmnt.Chkmnt import Chkmnt
from chkhealth.ChkHealth import ChkHealth

class Menu(object):
  '''
  Main menu for choosing actions.
  '''
  # some declarations
  __checkMount = None
  __checkHealth = None
  
  # Main definition
  __menu_actions = {}
  
  mainMenuLabels = ["Please choose the action you want to launch:", 
                           "1. Check and Deactivate AUTOMOUNT", 
                           "2. Perform SMART Health Test",
                           "\n0. Quit"]
  
  checkMountLabels = ["Before connecting the Disk disable Windows AUTOMOUNT\n",
                              "1. Check AUTOMOUNT",
                              "2. Disable AUTOMOUNT",
                              "3. Enable AUTOMOUNT",
                              "9. Back",
                              "0. Quit"
                              ]
  checkHealthLabels = ["Perform SMART Health Test",
                              "1. SMART Health test with smartctl \n",
                              "2. Open dd shell\n",
                              "9. Back",
                              "0. Quit"
                              ]

  def __init__(self):
    
    '''
    Menu entries definitions and initialize Classes
    '''
    
    self.__checkMount = Chkmnt()
    self.__checkHealth = ChkHealth()

    
    self.__chkHealth_menu = {
        '1':self.__checkHealth.initialize,
        '2':self.__checkHealth.initialize,
        '9':self.back,
        '0':self.exit,
    }
    
    self.__chkmnt_menu = {
        '1':self.__checkMount.check,
        '2':self.__checkMount.deactmnt,
        '3':self.__checkMount.actmnt,
        '9':self.back,
        '0':self.exit,
    }

    # Menu definition
    self.__menu_actions = {
        'main_menu': self.main_menu,
        '1': self.chkmnt,
        '2': self.health,
        'chkmnt': self.__chkmnt_menu,
        'chkhealth': self.__chkHealth_menu,
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
      # ch = choice.lower()
      if ch[0] == '':
          self.__menu_actions['main_menu']()
      else:
          try:
              # execute selected action  
              self.get_in_dic(ch)
              # self.__menu_actions[ch]()
          except KeyError:
              print "Invalid selection, please try again.\n"
              self.__menu_actions['main_menu']()
      return
  
  # Util to call a method up to 2nd depth level
  def get_in_dic(self, ch):
    mn = self.__menu_actions
    if ch[0] in mn:
      #if this is a second level menu
      if len(ch) > 1:
        if ch[1] in mn[ch[0]]:
          #then go to second level choice
          mn[ch[0]][ch[1]]()
      else:
        # go to first level choice
        mn[ch[0]]()
    #get back to main menu by default
    mn['main_menu']()
    return
  
#   def launcher(self, action):
#       if action == '':
#           self.__menu_actions['main_menu']()
#       else:
#           try:
#               self.__checkMount[action]()
#           except KeyError:
#               print "Invalid action, please try again.\n"
#               self.__menu_actions['main_menu']()
   
  # Menu for check AUTOMOUNT
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
      choice = ['chkhealth' , choice.lower()]
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
    # tmp = os.system('cls' if os.name=='nt' else 'clear')
    sp.call('cls', shell=True)
