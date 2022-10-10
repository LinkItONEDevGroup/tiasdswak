# @file cli.py
# @brief CLI of whole tool
# @author wuulong@gmail.com
#standard
import cmd
import logging


#extend
#import pandas as pd
#import pandasql as ps
import geopandas
from shapely.geometry import *

#library
import codes.globalclasses as gc
from codes.const import *
#from codes.db import *
from codes.lib import *




DOMAIN_SET_LOAD_SKIP=0
DOMAIN_SET_LOAD_CSV=1
DOMAIN_SET_LOAD_GEO=2

CX_DICT_LOAD_SKIP=0


##### Code section #####
#Spec: about, user commands, test commands
#How/NeedToKnow:
class Cli(cmd.Cmd):
    def __init__(self,stdout=None):
        cmd.Cmd.__init__(self)
        self.cli_tool = CliTool(stdout)
        self.cli_tbn = CliTbn(stdout)

        self.prompt = 'TiasdCLI>'

############ cli maintain ####################        
    def do_about(self, line):
        """About this software"""
        print("%s version: v%s" %(TITLE,VERSION))
    def do_quit(self, line):
        """quit"""
        return True
############ top command ####################                      
    def do_reset(self,line):
        """ reset for next run """  
        gc.GAP.reset()
        print("reseted")
    def do_reload_setting(self,line):
        """reload setting from INI"""
        gc.SETTING.reload()
        pd.set_option('display.max_rows', int(gc.SETTING["MAX_ROWS"]))
        pd.set_option('display.max_columns', int(gc.SETTING["MAX_COLUMNS"]))
        pd.set_option('display.max_colwidth', int(gc.SETTING["MAX_COLWIDTH"]))

    def do_displayall(self,line):
        """set record display all or brief
        0: brief, 1: all, row: all rows, col: all columns
displayall [0/1/row/column]
ex: display 1
        """
        if line=="0":
            gc.SETTING.reload()
            pd.set_option('display.max_rows', int(gc.SETTING["MAX_ROWS"]))
            pd.set_option('display.max_columns', int(gc.SETTING["MAX_COLUMNS"]))
            pd.set_option('display.max_colwidth', int(gc.SETTING["MAX_COLWIDTH"]))
        elif line=="row":
            pd.set_option('display.max_rows', None)
        elif line=="col":
            pd.set_option('display.max_columns', None)
        else:
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            #pd.set_option('display.max_colwidth', 0)

    def do_tool(self,line):
        """sys sub command directory"""
        self.cli_tool.prompt = self.prompt[:-1]+':tool>'
        self.cli_tool.cmdloop()
    def do_tbn(self,line):
        """tbn sub command directory"""
        self.cli_tbn.prompt = self.prompt[:-1]+':tbn>'
        self.cli_tbn.cmdloop()
############ tool sub cmd ####################
class CliTool(cmd.Cmd):
    def __init__(self,stdout):
        if stdout:
            cmd.Cmd.__init__(self,stdout=stdout)
        else:
            cmd.Cmd.__init__(self)

    def do_dbreload(self,line):
        """dbreload : reload db and save CSV
dbreload [b_save]
    [b_save] 1: save to include/台灣外來入侵種資料集 - 合併補充資料集.csv, 0: not save (default)
ex: dbreload 1
        """
        pars=line.split()
        b_save=0
        if len(pars)==1:
            if pars[0]=='1':
                b_save=1
        gc.TIASD.reload(b_save)
    def do_sql(self,line):
        """apply sql to select, default save result to output/query.csv
sql [sql_cmd]
ex: sql select * from df where common_name_c='埃及聖䴉'
ex: sql select * from df where "類別-動物"='鳥類'
ex: sql select * from df where "棲地類型Habitat types" like '%農業區%'
ex: sql select * from df where class_c='鳥綱' and common_name_c like '%八哥%'

        """
        #sql = line.replace("\"","")
        sql = line
        df = gc.TIASD.df_merge
        gc.TIASD.df_cur = sqldf(df, sql, "output/query.csv")
    def do_list(self,line):
        """list : list content of db
list [db_name] [content]
    [db_name] standard:政府資料 ,append:民間資料庫 ,extend:補充資料 ,mix= 政府+民間,merge= 政府+民間+補充 ,cur:目前查詢結果(default)
    [content] 0: show info, 1: show content (default)
ex: list cur 0
        """
        pars=line.split()
        db_name="cur"
        content=1
        if len(pars)>=1:
            db_name = pars[0]
            if len(pars)>=2:
                content = int(pars[1])
        df = gc.TIASD.get_df(db_name)
        if df is not None:
            if content==1:
                print(df.to_markdown())
            else:
                print("\n".join(list(df.columns)))

    def do_quit(self, line):
        """quit this sub command"""
        """quit"""
        return True

############ tool sub cmd ####################
class CliTbn(cmd.Cmd):
    def __init__(self,stdout):
        if stdout:
            cmd.Cmd.__init__(self,stdout=stdout)
        else:
            cmd.Cmd.__init__(self)

    def do_get_taxon(self,line):
        """"get_taxon : get taxonUUID by name_code
get_taxon [name_code]
    [name_code] (default: 419665)
ex: get_taxon 419665
"""
        pars=line.split()
        name_code=419665
        if len(pars)>=1:
            name_code=pars[0]

        json_all = namecode_to_taxonUUID(name_code)
        if json_all:
            taxonUUID=json_all['data'][0]['taxonUUID']
            print("name_code(%s)->taxonUUID(%s)" %(name_code,taxonUUID))

    def do_getcnt(self,line):
        """"getcnt : get name_code's occurrence count 
getcnt [name_code] : (default: current name_codes in result of sql command)
ex: getcnt 419665
"""
        pars=line.split()
        name_code=419665
        if len(pars)==1:
            name_code=pars[0]

            [taxonUUID,total,info]=getcnt_by_namecode(name_code)
            print("name_code(%s)->taxonUUID(%s) , cnt=%i" %(name_code,taxonUUID,total))
        else:
            df_cur = gc.TIASD.df_cur
            df_cur['name_info']=df_cur['name_code'] +":" +  df_cur['common_name_c']
            name_codes = gc.TIASD.df_cur['name_info'].tolist()
            for name_code in name_codes:
                [taxonUUID,total,info]=getcnt_by_namecode(name_code)
                print("name_code(%s)->taxonUUID(%s) , cnt=%i, info=%s" %(name_code,taxonUUID,total,info))

    def do_tbn_his(self,line):
        """"tbn_his : get taxonUUID's occurrence count history
tbn_his [taxonUUID] [days] [count]
    [taxonUUID] (default:233a25cd-bac6-4bb2-94bb-a4b4c173c218)
    [days] (default: 365.25)
    [count] (default: 3)
ex: tbn_his 233a25cd-bac6-4bb2-94bb-a4b4c173c218 365.25 3
"""
        taxonUUID="233a25cd-bac6-4bb2-94bb-a4b4c173c218"
        days = 365.25
        count = 3
        pars=line.split()
        if len(pars)>=1:
            taxonUUID=pars[0]
            if len(pars)>=2:
                days = float(pars[1])
                if len(pars)>=3:
                    count = int(pars[2])

        [url_t,grp_info] = tbn_his(taxonUUID,days,count)
        grp_total = tbn_getcnt_bygrp(url_t,grp_info,False)
        for item in grp_total:
            print("%s:%s" %(item, grp_total[item]))

    def do_quit(self, line):
        """quit this sub command"""
        """quit"""
        return True
