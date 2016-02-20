ParserModel
========

ParserModel is a tools for crawler extracting information from web though a specific XML documents. You can get a extracter only with a XML files with configuration. It's made by Python language, and it can easy to use as modular embedded in craweler framwork. 

********
Usage
--------

This is exmaple of ParserModel usage under the test file.

Exmaple of Code:

    #!/usr/bin/env python3
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

    #load xml files
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
            print("Time：%f"%(time.clock()-t1))

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


How to write correct XML files?
-------------------------------

XML file include three levels:

* Website is the topest, which describes the web page include url pattern, domain and host.
* data-object and outlink is the second level. It marking the names and types of extracting data, and update interval of url etc..
* xpath is the third level. It include some method of extracting data, like Xpath expression, string slice, regular expression and Python script.


Example of XML template:

    <?xml version="1.0" encoding="UTF-8"?>  

    <websites>  
        <website domain="" host="" paser-engine="xpath">
            <!--  -->
            <url-pattern>url-pattern-1</url-pattern>
            <url-pattern>url-pattern-2</url-pattern>
            <url-pattern>url-pattern-3</url-pattern>
            <!-- indicate how to retrieve data from page -->
            <data-object>
                <!-- occur value must in {"mandatory", "optional"}, default is "optional" -->
                <!-- data-type value must in {"string", "int", "float", "boolean"}, default
                    is "string"-->
                <field name="title" data-type="string" multi-value="false" occur="mandatory"
                    description="new's title">
                    <!-- list of expression -->
                    <xpath>
                        <expression>xpath expression</expression>
                        <!-- optional tags: start & end -->
                        <str-range start="" end="" />
                        <regular-match>abc</regular-match>
                        <script-name>function_name<script-name>
                    </xpath>
                    <xpath>
                        <expression>xpath expression</expression>
                        <!-- optional tags: start & end -->
                        <str-range start="" end="" />
                        <script><![CDATA[
                        ]]>
                        </script>
                    </xpath>
                </field>
                <field name="author" multi-value="false" occur="mandatory"
                    description="new's author">
                    <xpath>
                        <expression>xpath</expression>
                    </xpath>
                </field>
            </data-object>
            
            <!-- indicate how to retrieve outlink from page -->
            <outlinks>
                <!-- normalize value must in {"none", "default", "user-function"}, default
                    is "none"-->
                <entity occur="mandatory" trace="true" normalize="none" update-interval="-1">
                    <xpath>
                        <expression>//DIV[@id='pageDivTop']/A</expression>
                        <regular-match>abc</regular-match>
                    </xpath>
                    <xpath>
                        <expression>//DIV[@id='pageDivTop']/A</expression>
                        <regular-match>abc</regular-match>
                    </xpath>
                </entity>
                <entity>
                    <xpath>
                        <expression>//DIV[@id='pageDivTop']/A</expression>
                        <regular-match>abc</regular-match>
                    </xpath>
                </entity>
            </outlinks>
        </website>  
    </websites>



****************************

中文文档
========

ParserModel是一个网页解析模板库，通过编写一个简单的XML文件模板就可以实现对页面的解析，ParserModel是由Python语言写的，因此可以很容易的嵌入到Scrapy，PySpider等Python爬虫框架当中使用，当然也可以是你自己的爬虫框架。



用法
------------------

下面用一个ParserModel的案例说明ParserModel的用法,下面一个房客网的简单爬虫：

    #!/usr/bin/env python3
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

    #load xml files
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
            print("Time：%f"%(time.clock()-t1))

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


我们可以看到，ParserModel只需要通过加载XML文件就可以自动帮助我们爬取所需要的内容并存储在一个字典当中，实际就是将语言代码的编写转换成了统一的XML文件的编写工作。
那么这种特定的XML文件模板要如何编写呢?



XML模板文件编写
------------------

本文的XML文件主要分为三个层次：

* 最上面的一层为 网页解析。这一层主要用来描述 能够被后面步骤解析的URL，过滤掉无效的URL。
* 第二层为 数据描述层。 这一层主要用于描述 数据的属性，比如名称、存储类型、是否能为空、URL的更新周期等。
* 第三层是 数据解析层。 这一层主要是对数据的解析，包括Xpath表达式、字符串切片、正则表达式、Python脚本等。


下面展示上面代码的XML文件模板：

    <?xml version="1.0" encoding="UTF-8"?>  

    <websites>  
        <website domain="gz.fang.anjuke.com" paser-engine="xpath">
            <!--  -->
            <url-pattern>http://gz.fang.anjuke.com/loupan/s\?p=.*</url-pattern>
            <!-- indicate how to retrieve data from page -->
            <!-- indicate how to retrieve outlink from page -->
            <outlinks>
                <entity occur="optional" trace="true" normalize="none" update-interval="-1">
                    <xpath>
                        <expression>.//*[@id='container']/div[2]/div[1]/div[4]/div/a</expression>
                    </xpath>
                </entity>
                <entity occur="optional" trace="true" normalize="none" update-interval="-1">
                    <xpath>
                        <expression>.//*[@id='container']/div[2]/div[1]/div[3]/div/div[1]/div[1]/h3/a</expression>
                    </xpath>
                </entity>
            </outlinks>
        </website>  
        <website domain="gz.fang.anjuke.com" paser-engine="xpath">
            <!--  -->
            <url-pattern>http://gz.fang.anjuke.com/loupan/\d+</url-pattern>
            <!-- indicate how to retrieve data from page -->
            <!-- indicate how to retrieve outlink from page -->
            <data-object>
                <!-- occur value must in {"mandatory", "optional"}, default is "optional" -->
                <!-- data-type value must in {"string", "int", "float", "boolean"}, default
                    is "string"-->
                <field name="楼盘名称" data-type="string" multi-value="true" occur="mandatory"
                    description="小区名称">
                    <!-- list of expression -->
                    <xpath>
                        <expression>.//*[@id='j-triggerlayer']</expression>
                    </xpath>
                </field>
                
                <field name="价格" multi-value="true" occur="optional"
                    description="价格,单位:元/m2">
                    <xpath>
                        <expression>.//*[@id='container']/div[1]/div[2]/div[1]/dl/dd[1]</expression>
                        <regular-match>(\d+)元</regular-match>
                    </xpath>
                </field>
                <field name="户型" multi-value="true" description="户型">
                    <!-- list of template -->
                    <xpath>
                        <expression>.//*[@id='container']/div[1]/div[2]/div[1]/dl/dd[3]/div/a</expression>
                    </xpath>
                </field>
                <field name="地址" multi-value="true" description="地址">
                    <!-- list of template -->
                    <xpath>
                        <expression>.//*[@id='container']/div[1]/div[2]/div[1]/dl/dd[4]/span</expression>
                    </xpath>
                </field>
                <field name="电话" multi-value="true" description="电话">
                    <!-- list of template -->
                    <xpath>
                        <expression>.//*[@id='j-triggerlayer-b']/div/p/strong[1]</expression>
                    </xpath>
                </field>
                <field name="开盘日期" multi-value="true" description="开盘日期">
                    <!-- list of template -->
                    <xpath>
                        <expression>.//*[@id='container']/div[1]/div[2]/div[4]/ul[1]/li[1]</expression>
                    </xpath>
                </field>
                <field name="交房日期" multi-value="true" description="交房日期">
                    <!-- list of template -->
                    <xpath>
                        <expression>.//*[@id='container']/div[1]/div[2]/div[4]/ul[2]/li[1]/span</expression>
                    </xpath>
                </field>
            </data-object>
        </website>
    </websites>