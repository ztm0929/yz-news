import requests
from bs4 import BeautifulSoup
import csv

with open(f'yz-news/info.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['文章标题', '发布时间', '原文链接'])
    writer.writeheader()

baseurl = 'https://yz.chsi.com.cn'
url = 'https://yz.chsi.com.cn/kyzx/kydt/?start=0'

content = requests.get(url).text
soup = BeautifulSoup(content, 'lxml')

# items = soup.find_all('li')
items = soup.find('ul', class_='news-list').find_all('li')

for index, item in enumerate(items):
    infolist = []
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
    # infolist = infolist.append(info)
    # # df = pd.DataFrame(info)
    # # df.to_csv('info.csv')
    with open(f'yz-news/info.csv', 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=info.keys())
        writer.writerow(info)