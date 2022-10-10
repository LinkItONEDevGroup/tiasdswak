# @file lib.py
# @brief default library module
# @author wuulong@gmail.com
import os
import json
from datetime import datetime,date,timedelta
import pandas as pd
import pandasql as ps
import requests

def url_get(filename,url,reload=False,detail=False):
    if not os.path.isfile(filename) or reload:
        if detail:
            print("Getting %s to %s" %(url,filename))
        t1 = datetime.now()
        r = requests.get(url, params = {})
        open(filename, 'wb').write(r.content)
        t2 = datetime.now()
        #print("[%s]-%s" %(t2-t1,filename))

def load_json(filename):
    data = None
    try:
        data_date = ""
        with open(filename , 'r', encoding='UTF-8') as json_file:
            data = json.load(json_file)
            return data
    except:
        print("%s:%s" %(filename,"EXCEPTION!"))
        return None

def sqldf(df,sql,filename=''):
    try:
        print("sql=%s, filename=%s" %(sql,filename))
        m1_df= ps.sqldf(sql, locals())
        print(m1_df.to_markdown())
        #print(m1_df)
        if not filename=='':
            m1_df.to_csv(filename)
            print("CSV file saved: %s" %(filename))
        return m1_df
    except:
        print("EXCEPTION: sql=%s" %(sql))

# get data
def tbn_byurl(url,limit_break=0):
    #limit_break=30 #>0 can limit total
    load_cnt=0
    delay_secs=0
    #need_save=True
    pass_break=False

    filename_t="output/tbn_%i.json"

    while True:
        #if renew_url==True:
        #    url= url_t %(ver,str1,limit)
        filename  = filename_t %(load_cnt)
        print("filename=%s,url=%s" %(filename, url))
        url_get(filename, url,True)
        json_all = load_json(filename)
        if json_all['meta']['status']!="SUCCESS":
            print(json_all)
            break
        print("total=%i,itemsCount=%i,load_cnt=%i" %(json_all['meta']['total'],json_all['meta']['itemsCount'],load_cnt))

        if load_cnt==0:
            total = json_all['meta']['total']
            d={}
        for i in range(len(json_all['data'])):
            record_cur = json_all['data'][i]
            #print("%i: %s " %(i, record_cur))
            for key in record_cur.keys():
                if not key in d.keys():
                    #print("key=%s" %(key))
                    d[key]=[]
                d[key].append(record_cur[key])
            load_cnt += 1
        #load_cnt += records_cnt
        print("load_cnt=%i" %(load_cnt))
        if load_cnt >= total or (limit_break>0 and load_cnt >= limit_break):
            pass_break=True
            break
        url = json_all['links']['next']
        if delay_secs>0:
            print("current time : %s, need sleep %i second" % (time.ctime(),delay_secs))
            time.sleep(delay_secs)

    if pass_break==True:
        df = pd.DataFrame.from_dict(d)
        #df_to_db('table_name',df,'replace')
        return df
    else:
        return None
#分析，一組循序去查，得到的 summary
def tbn_bygrp(url_t,grp_info):
    df_all = None
    for item in grp_info.keys():
        url=url_t %(grp_info[item])
        df = tbn_byurl(url)
        if df_all is None:
            df_all=df
        else:
            df_all = pd.concat([df_all,df])
    return df_all
def tbn_getcnt_bygrp(url_t,grp_info,detail=True):

    grp_total={}
    filename_t="output/tbn_%s.json"

    for item in grp_info.keys():
        url=url_t %(grp_info[item])
        filename  = filename_t %(item)
        if detail:
            print("filename=%s,url=%s" %(filename, url))
        else:
            print("getting...%s" %(item))
        url_get(filename, url,True)
        json_all = load_json(filename)
        if json_all['meta']['status']!="SUCCESS":
            if detail:
                print(json_all)
            grp_total[item]=0
        else:
            print("total=%i" %(json_all['meta']['total']))
            grp_total[item]=json_all['meta']['total']

    return grp_total
# taibnet name_code to TBN taxonUUID
# https://www.tbn.org.tw/api/v25/taxon?taiCoLNameCode=419665
def namecode_to_taxonUUID(name_code,detail=False):
    url="https://www.tbn.org.tw/api/v25/taxon?taiCoLNameCode=%s" %(name_code)
    filename  = "output/namecode_%s.json" %(name_code)
    if detail:
        print("filename=%s,url=%s" %(filename, url))
    url_get(filename, url,True)
    json_all = load_json(filename)
    if json_all['meta']['status']=='SUCCESS':
        return json_all
    else:
        print(json_all)
        return None

def getcnt_by_namecode(name_code,detail=False):
    # [format] name_code:info , infor can be omit
    pars=name_code.split(':')
    info=''
    if len(pars)>=2:
        name_code = pars[0]
        info = pars[1]
    json_all = namecode_to_taxonUUID(name_code)
    if json_all:
        taxonUUID=json_all['data'][0]['taxonUUID']
        #print("name_code(%s)->taxonUUID(%s)" %(name_code,taxonUUID))

        url="https://www.tbn.org.tw/api/v25/occurrence?taxonUUID=%s&limit=20" %(taxonUUID)
        filename  = "output/taxonUUID_%s.json" %(taxonUUID)
        if detail:
            print("filename=%s,url=%s" %(filename, url))
        url_get(filename, url,True)
        json_all2 = load_json(filename)
        if json_all2['meta']['status']=='SUCCESS':
            total = json_all2['meta']['total']
            #print("total=%i" %(total))
        else:
            print("name_code(%s) can't find total" %(name_code))
            total = 0
        return [taxonUUID,total,info]
    else:
        print("name_code(%s) can't find taxonUUID" %(name_code))
        return ['',0,'']

def tbn_his(taxonUUID,days,count):
    # 每五年取得筆數
    date_cur = datetime.now()
    #taxonUUID="233a25cd-bac6-4bb2-94bb-a4b4c173c218"
    url_t="https://www.tbn.org.tw/api/v25/occurrence?taxonUUID=%s" %(taxonUUID) + "&eventDate=%s&limit=20"
    date_strs=[date_cur.strftime("%Y-%m-%d")]
    grp_info={}
    for i in range(count):
        date_prev = date_cur + timedelta(days = -days*(i+1))
        date_strs.append(date_prev.strftime("%Y-%m-%d"))
        par_str="%s~%s" %(date_strs[i+1],date_strs[i])
        url=url_t %(par_str)
        grp_info[par_str]=par_str
        print(url)
    return [url_t,grp_info]