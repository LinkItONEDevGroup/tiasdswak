# 工具安裝與說明

## 先從 github tiasdswak 下載

安裝建議使用 anaconda 套件環境

使用以下命令安裝：

- 先更改 environment.yml 內的 name, prefix，改成自己喜歡的環境名稱與路徑  

```sh
conda env create -f environment.yml 
```

- 如果出問題需要看確認可行的環境，可參考開發者環境狀態(預計主要版本都會更新 environment_detail.yml, 如果有更新的話)，此檔案由以下命令產生

```sh
conda env export > environment_detail.yml
```

- 環境升級參考命令

```sh
conda env update -n tiasdswak -f environment.yml
```

- 環境簡要說明

## 版本

目前程式版本為 V0.2，資料版本為：2023Q1.a1

## 釋出流程與方法

- 匯出 台灣外來入侵種資料集 (回覆)
    - 如果有更新
        - 外來入侵種民間資料庫
        - 台灣物種名錄-台灣外來物種
- tiasdswak tool/dbreload 1
    - 產生 include/台灣外來入侵種資料集 - 合併補充資料集.csv saved
    - 匯入 台灣外來入侵種資料集 - 合併補充資料集
- tiasdswak.ipynb 產製報表 *.md
- 用 Obsidian 個別產生 pdf
- github commit
    -包含 include 與 md/pdf
- [台灣外來入侵種資料集](https://drive.google.com/open?id=1dsLBu-q9tyDqMeVFMWUGmyhvqFYwXmcrK4L0HlRiz2M&usp=drive_copy) 標記版號
- [台灣外來入侵種資料集](https://docs.google.com/spreadsheets/d/1FFHZNCVA-uAINYYCOjtsCY2_UuyclPejH_Mh9WfEVR0/edit?resourcekey=undefined#gid=1890334775) (回覆) 標記版號
- 上傳 drive/釋出


## 使用須知

工具箱主要提供兩種工具，CLI 給不會寫python 的使用者，notebook 給熟悉 python 的使用者。
兩者目的不同： CLI 主要是將常用的功能提供給使用者使用， notebook 則是提供彈性的開發者支援，方便會寫程式的使用者，做更多的資料分析

## CLI使用手冊

### 設定

```
# pandas setting
MAX_ROWS=10 #60
MAX_COLUMNS=8 #20
MAX_COLWIDTH=50 #50
```
### 功能

- tool
    - 列出 standard:政府資料 ,append:民間資料庫 ,extend:補充資料 ,mix= 政府+民間,merge= 政府+民間+補充 ,cur:目前查詢結果(default)
    - 可針對資料集使用 sql 來查詢，並存成 CSV
    - name_code 轉換 taxonUUID
- tbn
    - 取得 name_code 在 TBN 目前的觀察數量
    - 取得 taxonUUID 的數量 （每隔固定間隔時間）


### 命令與使用範例

```sh
$ python tiasdswak.py
root        : INFO     LASS - TiasdSWAK version: v0.1
TiasdCLI>help

Documented commands (type help <topic>):
========================================
about  displayall  help  quit  reload_setting  reset  tbn  tool

TiasdCLI>about
TiasdSWAK version: v0.1
TiasdCLI>tool
TiasdCLI:tool>help

Documented commands (type help <topic>):
========================================
dbreload  help  list  quit  sql

TiasdCLI:tool>help list
list : list content of db
list [db_name] [content]
    [db_name] standard:政府資料 ,append:民間資料庫 ,extend:補充資料 ,mix= 政府+民間,merge= 政府+民間+補充 ,cur:目前查詢結果(default)
    [content] 0: show info, 1: show content (default)
ex: list cur 0
        
TiasdCLI:tool>help sql
apply sql to select, default save result to output/query.csv
sql [sql_cmd]
ex: sql select * from df where common_name_c='埃及聖䴉'
ex: sql select * from df where "類別-動物"='鳥類'
ex: sql select * from df where "棲地類型Habitat types" like '%農業區%'
ex: sql select * from df where class_c='鳥綱' and common_name_c like '%八哥%'

        
TiasdCLI:tool>sql select * from df where common_name_c='埃及聖䴉'
sql=select * from df where common_name_c='埃及聖䴉', filename=output/query.csv
|    |   name_code | kingdom   | kingdom_c   | phylum   | phylum_c   | class   | class_c   | order          | order_c   | family            | family_c   | genus        | genus_c   | name                                 | species     | infraspecies_marker   | infraspecies   | infraspecies2_marker   | infraspecies2   | author         | author2   | common_name_c   |   is_alien |   is_invasive |   is_cultivated | is_endemic   | cites_code   | iucn_code   | coa_code   | 時間戳記               | 電子郵件地址      | life_type   | life_type_animal   | life_type_plant   | habitat_types   | 棲地類型-中文其他   | 棲地類型-英文其他   | reference                                                                                                                                                         | description   | suggestion   | note                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | introduction_type   | introduction_cause   | introduction_vector   | introduction_date                                                                                                               | introduction_people       | found_date   | introduction_desc   | invasiveness   | mechanism   | outcome   | dispersal_mechanisms                                                                                                                                                                                                                        | eradication_methods   | tbd1   | tbd2   | description.1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | summary                                                                                                                                                                                 | tbd3                                                                                         | tbd4                                                                                                                                                                            | habitat_description                                                                                                                                                                                                                                                                                                                                        | nutrition                                                                                                                                                                                                                                                                                                                                                                                                                                                 | reproduction                                                                                                                                                                                                                                                                                                                                          | life_cycle                                                                                                                                                                                    | species_status                                                                                                                                                                                                                                                                                                                                     |
...

CSV file saved: output/query.csv
TiasdCLI:tool>quit
TiasdCLI>help

Documented commands (type help <topic>):
========================================
about  displayall  help  quit  reload_setting  reset  tbn  tool

TiasdCLI>tbn
TiasdCLI:tbn>help

Documented commands (type help <topic>):
========================================
get_taxon  getcnt  help  quit  tbn_his

TiasdCLI:tbn>help get_taxon
"get_taxon : get taxonUUID by name_code
get_taxon [name_code]
    [name_code] (default: 419665)
ex: get_taxon 419665
"
```


```sh
TiasdCLI:tbn>get_taxon 419665
name_code(419665)->taxonUUID(71a2a98f-257e-4c20-9248-3136dffbdcab)
TiasdCLI:tbn>help getcnt
"getcnt : get name_code's occurrence count 
getcnt [name_code] : (default: current name_codes in result of sql command)
ex: getcnt 419665

TiasdCLI:tbn>getcnt 419665
name_code(419665)->taxonUUID(71a2a98f-257e-4c20-9248-3136dffbdcab) , cnt=370

TiasdCLI:tbn>help tbn_his
"tbn_his : get taxonUUID's occurrence count history
tbn_his [taxonUUID] [days] [count]
    [taxonUUID] (default:233a25cd-bac6-4bb2-94bb-a4b4c173c218)
    [days] (default: 365.25)
    [count] (default: 3)
ex: tbn_his 233a25cd-bac6-4bb2-94bb-a4b4c173c218 365.25 3

TiasdCLI:tbn>tbn_his 233a25cd-bac6-4bb2-94bb-a4b4c173c218 365.25 3
https://www.tbn.org.tw/api/v25/occurrence?taxonUUID=233a25cd-bac6-4bb2-94bb-a4b4c173c218&eventDate=2021-10-10~2022-10-10&limit=20
https://www.tbn.org.tw/api/v25/occurrence?taxonUUID=233a25cd-bac6-4bb2-94bb-a4b4c173c218&eventDate=2020-10-10~2021-10-10&limit=20
https://www.tbn.org.tw/api/v25/occurrence?taxonUUID=233a25cd-bac6-4bb2-94bb-a4b4c173c218&eventDate=2019-10-10~2020-10-10&limit=20
getting...2021-10-10~2022-10-10
total=10160
getting...2020-10-10~2021-10-10
total=39842
getting...2019-10-10~2020-10-10
total=30316
2021-10-10~2022-10-10:10160
2020-10-10~2021-10-10:39842
2019-10-10~2020-10-10:30316
```


### 重要指引

**如何更新 DB**

資料維護在[台灣外來入侵種資料庫建構討論](https://docs.google.com/spreadsheets/d/1dsLBu-q9tyDqMeVFMWUGmyhvqFYwXmcrK4L0HlRiz2M/edit?usp=sharing)，
將以下幾個頁籤個別匯出 CSV, 蓋過 include/* 對應的檔案

|  來源             | 覆蓋                           |
| ----------------- | ------------------------------ |
| [台灣外來入侵種資料集](https://docs.google.com/spreadsheets/d/1dsLBu-q9tyDqMeVFMWUGmyhvqFYwXmcrK4L0HlRiz2M/edit?usp=sharing) | include/台灣物種名錄-台灣外來物種.csv |
| 台灣物種名錄-台灣外來物種 | |
| [台灣外來入侵種資料集](https://docs.google.com/spreadsheets/d/1dsLBu-q9tyDqMeVFMWUGmyhvqFYwXmcrK4L0HlRiz2M/edit?usp=sharing) | include/外來入侵種民間資料庫.csv | 
| 外來入侵種民間資料庫 | |
| 補充資料 [目前填寫結果](https://docs.google.com/spreadsheets/d/1FFHZNCVA-uAINYYCOjtsCY2_UuyclPejH_Mh9WfEVR0/edit?resourcekey=undefined#gid=1890334775) | include/台灣外來入侵種資料庫補充資料集 - 補充資料.csv |

可用以下命令產出 台灣外來入侵種資料庫補充資料集 - 合併補充資料集.csv
tool/dbreload 1
    - 建議 DB 有更新時，可以執行一次，製作 台灣外來入侵種資料庫補充資料集 - 合併補充資料集.csv，這樣可以用 excel like 的工具查看資料。但並非必要

```sh
$ python aisswak.py
TiasdCLI>tool
TiasdCLI:tool>dbreload 1
include/台灣外來入侵種資料集 - 合併補充資料集.csv saved
```

## 開發工具使用手冊

```
conda activate  tiasdswak
$ jupyter notebook 
```

