# @file ut.py
# @brief The main unit test program of whole project
# @author wuulong@gmail.com

#standard
import unittest
#homemake
import codes.globalclasses as gc
from codes.const import *



##### Unit test section ####
#the test ID provide the order of testes. 
#Spec: 
#How/NeedToKnow:  
class UTGeneral(unittest.TestCase):
    #local
    #ID:0-99
    def test_001_setting_signature(self):
        print("\nCheck signature and to see program started")
        self.assertEqual(gc.SETTING["SIGNATURE"],'tiasdswak')

    def test_002_cli_help(self):
        gc.CLI.do_help("")
        self.assertEqual(True,True)        


