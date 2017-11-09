'''
Created on 09 nov 2017

@author: koelio
'''
import unittest
from bashm.menu import Menu
from chkmnt import Chkmnt


class menuTest(unittest.TestCase):


    def testMenus(self):
        """Test menu functionality.

        """
        menu = Menu()
    
        #self.assertEquals(len(menu.mainMenuLabels), 4)
        self.assertEquals(len(menu.checkMountLabels), 6)
        self.assertEquals(len(menu.checkHealthLabels), 5)      
    
#         expected_parts_string = (
#             u'00:  0000000000   0000000000   0000000001   Primary Table (#0)\n'
#             u'01:  0000000000   0000000000   0000000001   Unallocated\n'
#             u'02:  0000000001   0000000350   0000000350   Linux (0x83)\n'
#             u'03:  0000000351   0000002879   0000002529   DOS Extended (0x05)\n'
#             u'04:  0000000351   0000000351   0000000001   Extended Table (#1)\n'
#             u'05:  0000000351   0000000351   0000000001   Unallocated\n'
#             u'06:  0000000352   0000002879   0000002528   Linux (0x83)\n')
#     
#         self.assertEquals(u''.join(parts), expected_parts_string)

    def testMountMenu(self):
        """Test mount menu functionality.

        """
        chkmnt = Chkmnt()
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMenu']
    unittest.main()