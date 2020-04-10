# -*- coding: utf-8 -*

"""
目标，爬取全部的题目以及答案
1. 利用cookie访问网页，记录全部的题目id并记录在内存中 需要把标签的属性记下来
2. 依次访问这些题目的网页，爬取问题选项和答案
3. 存储到本地文件
"""

import requests
from lxml import etree
import re

def pageid(url, cookie):


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Cookie': cookie
    }

    session = requests.Session()

    response = session.get(url, headers=headers)

    # print(response.text)

    selector = etree.HTML(response.text)

    pagelinks = []

    for i in range(30):
        apageid = selector.xpath('/html/body/div[1]/div[2]/div[2]/div[1]/ul/li['+str(i+1)+']/a/@href')


        pagelinks.append('https://www.nowcoder.com'+"".join(apageid))

        # print(pagelinks)

    return pagelinks

def access(urls, cookie):

    for url in urls:

        print('\n'+url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'Cookie': cookie
        }

        session = requests.Session()

        response = session.get(url, headers=headers)


        selector = etree.HTML(response.text)

        question = re.sub("_计算机基础-链表,数组专项练习_牛客网|<span>|</span>|\n", '', selector.xpath('/html/head/title/text()')[0])

        rightans = re.findall("[ABCD]", selector.xpath('/html/body/div[1]/div[2]/div[2]/div[3]/h1/text()')[0])[0]

        print(question)

        print(rightans)
        for i in range(1, 5):

            content = selector.xpath('/html/body/div[1]/div[2]/div[2]/div[3]/div['+str(i)+']//text()')
            if len(content)<5 and content:

                answer = chr(ord('A')+(i-1))+':'+content[1]
                print(answer)

if __name__ == '__main__':

    cookie = 'NOWCODERUID=C1F47CBEB368100B259B00921BDE1A9C; NOWCODERCLINETID=2987429E46984C805C4B748D83F50505; Hm_lvt_a808a1326b6c06c437de769d1b85b870=1582727926,1582951795,1583150899,1583296142; callBack=%2Ftest%2Fquestion%2Fdone%3Ftid%3D31053807%26qid%3D171569%26headNav%3Dwww; Hm_lpvt_a808a1326b6c06c437de769d1b85b870=1583298317; t=2B8379AABDEFC411E988236C916DCA4B; SERVERID=11b18158070cf9d7800d51a2f8a74633|1583298320|1583296137'

    urls = pageid('https://www.nowcoder.com/test/question/done?tid=31053807&qid=171569', cookie)
    # print(urls)
    access(urls, cookie)

