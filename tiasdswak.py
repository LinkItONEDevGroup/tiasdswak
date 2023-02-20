## @file aisswak.py
# @brief  Tool to manage ais datasets
# AUTHOR: WuLung Hsu, wuulong@gmail.com
# CREATE DATE: 2022/9/27


#standard
import getopt
import sys
import unittest
import pandas as pd

#extend
from configobj import ConfigObj

#library
import codes.globalclasses as gc
from codes.const import *
import codes.app as app
import codes.cli as cli
import codes.ut as ut
import codes.ui as ui
from codes.lib import *

global apmode
apmode = AP_MODE_NOTEBOOK
class TiasdSwak():
    """
        Tool to manage ais datasets

    """
    def __init__(self):
        if apmode==AP_MODE_NOTEBOOK:
            print("%s-V%s" %(TITLE,VERSION))
        self.reload(False)
    def load(self):
        #load csv
        self.df_standard = pd.read_csv(DBFILE_STANDARD)
        self.df_append = pd.read_csv(DBFILE_APPEND)
        self.df_extend = pd.read_csv(DBFILE_EXTEND)
        self.df_extend = self.df_extend.astype({'name_code':'str'})
        self.df_group = pd.read_csv(FILE_GROUP)
        self.df_coldef = pd.read_csv(COL_DEF)
        self.gen_group()
    def gen_group(self):
        group={}
        for row in self.df_group.iterrows():
            group_name=str(row[1]['group_name'])
            name_code=str(row[1]['name_code'])
            if not group_name in group.keys():
                group[group_name]=[]
            group[group_name].append(name_code)
        self.group = group


    def mix(self):
        df_mix = self.df_standard
        for row in self.df_append.iterrows():
            name_code = str(row[1]['name_code'])
            #print(name_code)
            name_code_values=df_mix[df_mix['name_code']==name_code]['name_code'].values.tolist()
            if len(name_code_values) > 0: #delete match row
                #print("%s exist!" %(name_code))
                idx=df_mix.index[df_mix['name_code']==name_code].tolist()
                df_mix.drop(idx, axis=0, inplace=True)
        #self.df_mix=df_mix[df_mix['is_invasive']==1].append(self.df_append[self.df_append['is_invasive']==1])
        self.df_mix=pd.concat( [df_mix[df_mix['is_invasive']==1],self.df_append[self.df_append['is_invasive']==1]])

    def merge(self,b_save=False):

        self.df_merge = self.df_mix.join(self.df_extend.set_index('name_code'),on='name_code',how='outer',lsuffix='L',rsuffix='R')
        self.df_cur = self.df_merge
        self.df_dig = self.df_merge.copy()
        if b_save:
            self.df_merge.to_csv(DBFILE_MERGE,index=False)
            print("%s saved" %(DBFILE_MERGE))
    def reload(self,b_save=False):
        self.load()
        self.mix()
        self.merge(b_save)
    def get_df(self,db_name):
        db_namelist={'standard': self.df_standard
            ,'append': self.df_append, 'extend':self.df_extend, 'mix': self.df_mix, 'merge':self.df_merge,'cur':self.df_cur}
        if db_name in db_namelist.keys():
            return db_namelist[db_name]
        else:
            return None
    def test(self):
        df = self.df_merge
        sqldf(df,"select * from df where common_name_c='哈爸'")


if __name__ =='__main__':
    # Read system parameters which are assigned while we launching "start.py".
    # If the input parameter is invalid, then display usage and return "command
    # line syntax" error code.
    apmode = AP_MODE_NORMAL
    debug_mode = DEBUG_MODE_OFF

    #command line paramters handler
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht", [])
        for opt, arg in opts:
            if opt == '-h':
                print ('tiasdswak.py [ -h ] [ -t ]')
                print ('    -h, --help: help message')
                print ('    -t, --test: unit test mode')
                sys.exit()
            elif opt in ("-t", "--test"):
                apmode = AP_MODE_UNITTEST
                print("Running as unittest mode!")
    except getopt.GetoptError:
        print ('usage: tiasdswak.py [ -h ] [ -t ]')
        sys.exit(2)

        #init global classes
    gc.SETTING  = ConfigObj("include/tiasdswak.ini")
    gc.UI = ui.UserInterface()
    gc.GAP = app.SApp()
    gc.CLI = cli.Cli()
    gc.TIASD = TiasdSwak()


    #run by different mode
    if apmode == AP_MODE_UNITTEST:
        suite = unittest.TestLoader().loadTestsFromTestCase(ut.UTGeneral)
        unittest.TextTestRunner(verbosity = 2).run(suite)
    else:
        if debug_mode==DEBUG_MODE_ON:
            while 1:
                ret=1
                try:
                    ret = gc.CLI.cmdloop() #normal exit return None
                except:
                    print("Broken Safe Exception!")
                if ret is None:
                    break
        else:
            gc.CLI.cmdloop()




