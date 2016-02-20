# coding:utf8
import requests
import time
import ParserModel
import json
import hashlib

url_search = "http://epub.cnki.net/KNS/request/SearchHandler.ashx"
url_data = "http://epub.cnki.net/kns/brief/brief.aspx"
headers = {'Connection':'Keep-Alive',
           'Accept':'text/html,*/*',
           'User-Agent':'Mozilla/6.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
           'Referer':'http://epub.cnki.net/kns/brief/result.aspx?dbprefix=scdb&action=scdbsearch&db_opt=SCDB'}

payload_search = {'action': '',
                  'NaviCode': '*',
                  "ua":"1.21",
                  'PageName':'ASP.brief_result_aspx',
                  "DbPrefix": "SCDB",
                  'DbCatalog':'中国学术文献网络出版总库',
                  'ConfigFile':'SCDB.xml',
                  'db_opt': 'CJFQ,CJFN,CDFD,CMFD,CPFD,IPFD,CCND,CCJD,HBRD',
                  'base_special1':'%',
                  'magazine_value1': '电信科学',  # 杂志名称
                  'magazine_special1': '%',
                  'his':'0',
                  '__':time.strftime('%a %b %d %Y %H:%M:%S')+' GMT+0800 (中国标准时间)'
                  }

payload_data = {'pagename':'ASP.brief_result_aspx',
           'dbPrefix': 'SCDB',
           'DbCatalog': '中国学术文献网络出版总库',  # 搜索数据库
           'ConfigFile':'SCDB.xml',
           'research':'off',
           't':int(time.time()),
           'keyValue':'',
           'S':'1'}

s = requests.Session()
r_search = s.get(url_search, params=payload_search, headers=headers)
#将搜索句柄cookies传递给结果
r_data = s.get(url_data, params=payload_data, headers=headers)
##def save_html(html, name):
##    with open("test/"+name+".html","w",encoding="utf8") as f:
##        f.write(html.decode("utf8"))

#ParserModel模块测试
with open("CNKI_template.xml","r",encoding="utf8") as f:
    xml_file = f.read()
with open("url_normalize.py", encoding="utf8") as f:
    script = f.read()
parser = ParserModel.XMLParser()
parser.load_parsed_files(xml_file, script)
urls = [r_data.url]
finish_url = []

with open("result.json", "w" ,encoding="utf8") as f:
    result = {}
    result["data"] = []
    try:
        while True:
            url = urls.pop()
            if url in finish_url:
                continue
            #print(len(urls))
            #print(url)
            r = s.get(url, headers=headers)
            html_content = r.content.decode("utf8")
            t1 = time.clock()
            parser.parsering(url, html_content)
            print(u"CNKI爬虫中parser模块parsering方法时间：%f"%(time.clock()-t1))
            #去重
            if "outlink" in parser.result.keys():
                urls = list(set(urls + list(parser.result["outlink"].keys())))
            if "parsed-data" in parser.result.keys():
                result["data"].append(parser.result["parsed-data"])
            finish_url.append(url)
            time.sleep(3)
            if len(urls) == 0:
                break
    finally:
        f.write(json.dumps(result, ensure_ascii=False))
