# coding:utf8
import requests
import time
import ParserModel
import json

url_search = "http://gz.fang.anjuke.com/loupan/s?p=1"

headers = {'Connection':'Keep-Alive',
           'Accept':'text/html,*/*',
           'User-Agent':'Mozilla/6.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
           'Referer':'http://epub.cnki.net/kns/brief/result.aspx?dbprefix=scdb&action=scdbsearch&db_opt=SCDB'}

r_search = requests.get(url_search, headers=headers)

#ParserModel模块测试
with open("house_template.xml","r",encoding="utf8") as f:
    xml_file = f.read()

parser = ParserModel.XMLParser()
parser.load_parsed_files(xml_file)
urls = [r_search.url]
finish_url = []

with open("result.json", "w" ,encoding="utf8") as f:
    result = {}
    result["data"] = []
    while True:
        url = urls.pop()
        if url in finish_url:
            continue
        r = requests.get(url, headers=headers)
        html_content = r.content.decode("utf8")
        with open("./parser_model_profile_test/"+url[-1], "w") as f:
            print(url)
            f.write(html_content)
        t1 = time.clock()
        parser.parsering(url, html_content)
        print("搜房网爬虫中parser模块parsering方法时间：%f"%(time.clock()-t1))
        #去重
        if "outlink" in parser.result.keys():
            urls = list(set(urls + list(parser.result["outlink"].keys())))
        if "parsed-data" in parser.result.keys():
            #print(parser.result["parsed-data"])
            result["data"].append(parser.result["parsed-data"])
        finish_url.append(url)
        time.sleep(5)
        if len(urls) == 0:
            break
    f.write(json.dumps(result, ensure_ascii=False))
