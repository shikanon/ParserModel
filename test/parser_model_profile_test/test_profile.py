from multiprocessing.dummy import Pool as ThreadPool
import random
import ParserModel
import time
url = "http://gz.fang.anjuke.com/loupan/s?p=1"
with open("../house_template.xml","r",encoding="utf8") as f:
    xml_file = f.read()
with open("1.html", "r", encoding="utf8") as f:
    html_content = f.read()

parser = ParserModel.XMLParser()
parser.load_parsed_files(xml_file)
t1 = time.clock()
a = parser.parsering(url, html_content)
print(time.clock()-t1)
print(a)

class test:

    def run(self):
        result = {}
        t1 = time.clock()
        pool = ThreadPool(8)
##        for i in range(10):
##            a = self.test()
##            result[a] = i
        result = pool.map(self.test,range(10))
        print(time.clock()-t1)
        print(result)
        
    def test(self,i):
        time.sleep(0.5)
        return random.random()

a = test()
a.run()
