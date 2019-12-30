import requests
from lxml import etree
from datetime import datetime
from time import sleep

class Crawler(object):
    def __init__(self,
                 base_url='https://www.csie.ntu.edu.tw/news/',
                 rel_url='news.php?class=101'):
        self.base_url = base_url
        self.rel_url = rel_url

    def crawl(self, start_date, end_date,
              date_thres=datetime(2012, 1, 1)):
        """Main crawl API
        1. Note that you need to sleep 0.1 seconds for any request.
        2. It is welcome to modify TA's template.
        """
        if end_date < date_thres:
            end_date = date_thres
        contents = list()
        page_num = 0
        while True:
            rets, last_date = self.crawl_page(
                start_date, end_date, page=f'&no={page_num}')
            page_num += 10
            if rets:
                contents += rets
            if last_date < start_date:
                break
        return contents

    def crawl_page(self, start_date, end_date, page=''):
        #print("hello world")
        """Parse ten rows of the given page
        Parameters:
            start_date (datetime): the start date (included)
            end_date (datetime): the end date (included)
            page (str): the relative url specified page num
        Returns:
            content (list): a list of date, title, and content
            last_date (datetime): the smallest date in the page
        """
        res = requests.get(
            self.base_url + self.rel_url + page,
            headers={'Accept-Language':
                     'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        ).content.decode()
        sleep(0.1)
        # Todo add by Hermes: I know what to do below this line, but some technique problems are still required solution to solve. 
        root = etree.HTML(res)  
        dates = root.xpath('/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]/text()')
        titles = root.xpath('/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]/a/text()')
        rel_urls = root.xpath('/html/body/div[1]/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]/a/@href')
        contents = list()
        last_date = start_date
        for date, title, rel_url in zip(dates , titles, rel_urls):
            date = datetime.strptime(date, '%Y-%m-%d')
            if start_date <= date <= end_date:
                url = self.base_url + rel_url
                content = self.crawl_content(url)
                contents.append((date, title, content))
            else:
                last_date = date
                break
        # Todo add by Hermes: makes 'content' into a list called 'contents' and return
        
        return contents, last_date

    def crawl_content(self, url):
        t = requests.get(url).content.decode();
        html = etree.HTML(t)
        xpath = '//div[1]/div[2]/div/div/div[2]/div/div[2]//text()'
        content = html.xpath(xpath)
        return ' '.join(content)
        