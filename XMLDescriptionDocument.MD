
XML说明文档
=============


XML文件各类标签说明
--------------



**&lt;websites&gt;&lt;/websites&gt;**

一个用户的所有模板文件存放，里面可以包含多个&lt;website &gt;&lt;/website&gt;模板


**&lt;website&gt;&lt;/website&gt;**

一个网页抓取模板，主要包含了domain、host和paser-engine属性。
其中domain表示域名模式，如:sina.com, hao123.com等，host则表示域名全称，例如www.sina.com, news.sina.com等，domain和host两者至少需要有一个要填写，否则抛出文件错误异常，当两者都写时默认domain有效。paser-engine表示用何种格式进行解析，默认为xpath。


**&lt;url-pattern&gt;url-pattern-1&lt;/url-pattern&gt;**

url-pattern表示网页链接匹配的模式，url-pattern 可以为多个值，表达式为正则表达式形式。


**&lt;data-object&gt;&lt;/data-object&gt;**

定义如何从页面解析得到所需数据，可以包含多个&lt;field&gt;&lt;/field&gt;解析方法。


**&lt;field&gt;&lt;/field&gt;**

各字段包含信息，包含name，data-type，multi-value，occur，description五个属性。
name为数据存储字段名，name值必须存在否则抛出文件错误异常。
data-type为数据存储类型，仅支持string，int，float三种类型，默认为string。
multi-value表示存储数据是否为多值，默认为false。
occur表示所抓取数据是否必须存在，支持mandatory，optional两种类型。mandatory表示所抓数据不能为空否则抛出异常，optional则表示解析数据可以为空。默认为optional。
description对数据的描述，用于报错时快速锁定。
&lt;field&gt;&lt;/field&gt;下可以包含多个xpath解析，以循环形式遍历每个&lt;xpath&gt;&lt;/xpath&gt;
解析，直到成功则直接跳出。


**&lt;xpath&gt;&lt;/xpath&gt;**

xpath解析，&lt;expression&gt;&lt;/expression&gt;内部写xpath解析表示式，空则表示对全文进行采集。对解析后的文字处理包括了三种可选方法，分别为str-range字符串切片方法，regular-match 表示用正则表达式匹配，script用户自定义函数。
&lt;str-range start="" end="" /&gt;表示字符切片的开始字符和结束字符，如果start为空则表示从第一个开始，end为空表示到最后一个结束。
&lt;regular-match&gt;&lt;/regular-match&gt;表示对xpath抽取文字用正则表达式解析。如果为空，则不匹配。如果匹配结果有多个值，选择第一个值输出。
&lt;script-name&gt;&lt;script-name&gt;表示一个python代码函数名称。
&lt;script&gt;&lt;/script&gt;可以写入用户自定义python代码进行解析。代码必须以一个函数方式传入，函数名称必须为user_parser_function，传入一个字符串str，并返回一个字符串类型，否则抛出一个xml文件异样错误。
如果三个都存在，解析顺序为&lt;str-range start="" end="" /&gt;，&lt;regular-match&gt;&lt;/regular-match&gt;，&lt;script&gt;&lt;/script&gt;


**&lt;outlinks&gt;&lt;/outlinks&gt;**

获取外链，内可包含多个&lt;entity&gt;&lt;/entity&gt;外链解析。


**&lt;entity&gt;&lt;/entity&gt;**

外链解析，包含occur，trace，normalize，update-interval 四种属性。
occur表示所抓取数据是否必须存在，支持mandatory，optional两种类型。mandatory表示所抓数据不能为空否则抛出异常，optional则表示解析数据可以为空。默认为optional。
trace表示外链是否具有痕迹记录功能，true表示可记录痕迹，false表示不记录。默认为true。
normalize表示对外链是否进行规则化去重处理，包含none，default，user-function三种选择。none表示不对外链进行规则化去重处理，default表示使用默认方法对外链进行规则话去重处理，user-function表示自定义Python函数，函数必须命名为user_normalize_function，输入一个url，返回一个修正后的url值。默认为none。
update-interval表示外链更新间隔，单位为分钟，默认为-1，表示不更新。
&lt;entity&gt;&lt;/entity&gt;下可以包含多个xpath解析，以循环形式遍历每个&lt;xpath&gt;&lt;/xpath&gt;
解析，直到成功则直接跳出。
