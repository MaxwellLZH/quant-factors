import requests
from bs4 import BeautifulSoup
import logging
import shelve
from urllib.parse import urljoin
from datetime import datetime
from dateutil.parser import parse


logger = logging.getLogger(__file__)


INITIAL_URL = 'http://bbs.tianya.cn/list.jsp?item=stocks'


def get_articles(url):
	""" 爬取当前页面下的帖子信息，返回帖子信息的列表以及下一页的跳转链接 """
	resp = requests.get(url)
	if resp.status_code != 200:
		raise ValueError(resp.text)


	soup = BeautifulSoup(resp.text, 'lxml')

	articles = []
	for row in soup.find_all('tr'):
		d_row = {}

		cols = row.find_all('td')
		if len(cols) != 5:
			continue

		# 第一列标题
		tag = cols[0].find_all('a')[-1]
		link = tag['href']
		if not link.startswith('http'):
			link = urljoin('http://bbs.tianya.cn', link)
		d_row['title'] = tag.text.strip()
		d_row['article_link'] = link

		# 第二列作者
		tag = cols[1].find('a')
		d_row['author'] = tag.text
		d_row['author_link'] = tag['href']

		# 第三列点击量
		d_row['view_count'] = int(cols[2].text)

		# 第四列回复数
		d_row['reply_count'] = int(cols[3].text)

		# 第五列最新回复时间
		time = cols[4].text
		time = str(datetime.now().year) + '-' + time
		d_row['last_reply_time'] = parse(time)

		articles.append(d_row)

	next_page_link = soup.find('a', text='下一页')['href']
	next_page_link = urljoin('http://bbs.tianya.cn', next_page_link)
	logger.info('爬取成功: {}'.format(url))
	return articles, next_page_link
