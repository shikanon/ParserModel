# coding:utf8
import requests
import time
import ParserModel
import hashlib

url = "http://cjc.ict.ac.cn/qwjs/2015-all%20in%20one.htm"
r_data = requests.get(url)

#ParserModel模块测试
with open("cjc_template.xml","r",encoding="utf8") as f:
    xml_file = f.read()

parser = ParserModel.XMLParser()
parser.load_parsed_files(xml_file)
urls = [r_data.url]
finish_url = []

with open("result.json", "w", encoding="utf8") as f:
    t1 = time.time()
    result = {}
    result["data"] = []
    while True:
        t2 = time.time()
        url = urls.pop()
        if url in finish_url:
            continue
        if "pdf" in url:
            r = requests.get(url)
            with open("pdf/%s.pdf"%hashlib.md5(url.encode("utf8")).hexdigest(), "wb") as f:
                f.write(r.content)
        else:
            r = requests.get(url)
            t1 = time.clock()
            parser.parsering(url, r.content.decode("gb18030"))
            print("计算机学报爬虫中parser模块parsering方法时间：%f"%(time.clock()-t1))
            #去重
            if "outlink" in parser.result.keys():
                urls = list(set(urls + list(parser.result["outlink"].keys())))
                #print(parser.result["parsed-data"])
            finish_url.append(url)
            time.sleep(5)
            if len(urls) == 0:
                    break
