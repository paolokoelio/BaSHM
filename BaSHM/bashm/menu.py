'''
Created on 23 ott 2017

@author: koelio
'''
import subprocess as sp  # for screen cleaning (cls)
from chkmnt.Chkmnt import Chkmnt

class Menu(object):
  '''
  Main menu for choosing actions.
  '''
  # initilize
  __checkMount = None
  
  # Get confs, needed throughout the program
  __config = None
  
  # Main definition - constants
  __menu_actions = {}
  

  def __init__(self, config):
    
    '''
    Menu's entries definitions and initialize Classes
    '''
    self.__config = config
    
    # path = str(config.get('paths', 'static'))
    # print("YOYO" + path)
    
    self.__checkMount = Chkmnt(self.__config)
    
    self.__chkmnt_menu = {
        '1': self.__checkMount.check,
        '2':self.chkmnt,
        '9':self.back,
        '0':self.exit,
    }

          # Menu definition
    self.__menu_actions = {
        'main_menu': self.main_menu,
        '1': self.chkmnt,
        '2': self.menu2,
        'chkmnt': self.__chkmnt_menu,
        '9': self.back,
        '0': self.exit,
    }
    
  

  # =======================
  #     MENUS FUNCTIONS
  # =======================
   
  # Main menu
  def main_menu(self):
      cls()
      
      print "Welcome, to BaSHM\n"
      print "Please choose the action you want to start:"
      print "1. Check and Deactivate AUTOMOUNT"
      print "2. Menu 2"
      print "\n0. Quit"
      choice = raw_input(" >>  ")
      ch = [choice.lower()]
      self.exec_menu(ch)
   
      return
  
  def get_in_dic(self, ch):
    mn = self.__menu_actions
    if ch[0] in mn:
      if len(ch) > 1:
        if ch[1] in mn[ch[0]]:
          mn[ch[0]][ch[1]]()
      else:
        mn[ch[0]]()
   
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
  def launcher(self, action):
      if action == '':
          self.__menu_actions['main_menu']()
      else:
          try:
              self.__checkMount[action]()
          except KeyError:
              print "Invalid action, please try again.\n"
              self.__menu_actions['main_menu']()
   
  # CHeck AUTOMOUNT
  def chkmnt(self):
      print "Deactivate AUTOMOUNT\n"
      print "1. Check AUTOMOUNT"
      print "2. Deactivate AUTOMOUNT"
      print "9. Back"
      print "0. Quit"
      choice = raw_input(" >>  ")
      choice = ['chkmnt' , choice.lower()]
      self.exec_menu(choice)
      return
   
   
  # Menu 2
  def menu2(self):
      print "Hello Menu 2 !\n"
      print "9. Back"
      print "0. Quit" 
      choice = raw_input(" >>  ")
      choice = [choice.lower()]
      self.exec_menu(choice)
      return
   
  # Back to main menu
  def back(self):
      self.__menu_actions['main_menu']()
   
  # Exit program
  def exit(self):
      # sys.exit(0)
      return
    
def cls():
    # tmp = os.system('cls' if os.name=='nt' else 'clear')
    sp.call('cls', shell=True)
