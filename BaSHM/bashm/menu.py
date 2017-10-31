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
  
  # Get confs, needed throughout the program
  __config = None
  
  # Main definition - constants
  __menu_actions = {}
  

  def __init__(self, config):
    
    '''
    Menu entries definitions and initialize Classes
    '''
    self.__config = config
    
    # path = str(config.get('paths', 'static'))
    # print("YOYO" + path)
    
    self.__checkMount = Chkmnt(self.__config)
    self.__checkHealth = ChkHealth()

    
    self.__chkHealth_menu = {
        '1':self.__checkHealth.chkhealth,
        '2':self.__checkHealth.chkhealth,
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
    print("Hey")

  # =======================
  #     MENUS FUNCTIONS
  # =======================
   
  # Main menu
  def main_menu(self):
      if True:
        print "Welcome, to BaSHM\n"
      print "Please choose the action you want to launch:"
      print "1. Check and Deactivate AUTOMOUNT"
      print "2. Perform Health Test"
      print "\n0. Quit"
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
  
  # util to call a method up to 2nd depth level
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
      print "Before connecting the Disk disable Windows AUTOMOUNT\n"
      print "1. Check AUTOMOUNT"
      print "2. Disable AUTOMOUNT"
      print "3. Enable AUTOMOUNT"
      print "9. Back"
      print "0. Quit"
      choice = raw_input(" >>  ")
      choice = ['chkmnt' , choice.lower()]
      self.exec_menu(choice)
      return
   
   
  # Menu for Health check with SMART
  def health(self):
      print "Health test with SMART data \n"
      print "1. Health test with smartctl \n"
      print "2. Open dd shell\n"
      print "9. Back"
      print "0. Quit" 
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
