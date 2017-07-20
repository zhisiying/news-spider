import re
from urllib import request
from lxml import etree
import lxml

testurl="http://news.163.com/rank/"

with request.urlopen(testurl) as f:
    print('Status:', f.status, f.reason)
    #网页的编码格式只取一次，默认所有的编码方式都是这个
    decode=(f.headers['Content-Type'].split(';')[1]).split('=')[1]
    data = f.read().decode(decode.lower())
    infos = re.findall(r'<div class="titleBar" id=".*?"><h2>(.*?)</h2><div class="more"><a href="(.*?)">.*?</a></div></div>', data, re.S)
    for i in range(len(infos)):
        print('%s-%s'%(i,infos[i][0]))
    print('选择新闻类型')
    k=input()
    if k.isdigit()and int(k)<len(infos):
        newpage=(request.urlopen(infos[int(k)][1]).read()).decode(decode.lower())
        dom=etree.HTML(newpage)
        items=dom.xpath('//tr/td/a/text()')
        urls=dom.xpath('//tr/td/a/@href')
        assert (len(items)==len(urls))
        print(len(items))
        for i in range(len(urls)):
            print(items[i])
            new=(request.urlopen(urls[i]).read()).decode(decode.lower())
            ncs=re.findall(r'<div id="endText" class="end-text">.*?</div>',data,re.S)
            newdom=etree.HTML(new)
            newitems=newdom.xpath("//div[@id='endText'and @class='post_text']/p/text()")
            for n in newitems:
                print(n)
            print('=======================输入y继续')
            if 'y'==input():continue
            else:break;
