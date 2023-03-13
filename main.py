import requests
from bs4 import BeautifulSoup
import csv

#  创建 CSV 文件并填写表头，用于存放或获取到的信息，其中 encoding 需要设置为 ‘utf-8-sig’ ，否则Excel读取到中文会显示为乱码，下同；
with open(f'yz-news/info.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['文章标题', '发布时间', '原文链接'])
    writer.writeheader()

# 研招网官网，以及「考研动态」栏目的网址，后者50条新闻为一页，以此递增实现翻页；
baseurl = 'https://yz.chsi.com.cn'
url = 'https://yz.chsi.com.cn/kyzx/kydt/?start=0'

content = requests.get(url).text
soup = BeautifulSoup(content, 'lxml')

items = soup.find('ul', class_='news-list').find_all('li')

for item in items:
    # 原网页 html 中，标题和链接有分属于不同的 a 标签这一情况，故采用倒序索引的方式获取标题；
    title = item.find_all('a')[-1].text
    # if "初试" in title:
    published_time = item.find('span').text
    short_link = item.find('a')['href']
    link = baseurl + short_link
    info = {
        '文章标题': title,
        '发布时间': published_time,
        '原文链接': link,
    }
    # 打开先前已创建好的CSV文件，并开启追加模式，添加内容即可；
    with open(f'yz-news/info.csv', 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=info.keys())
        writer.writerow(info)