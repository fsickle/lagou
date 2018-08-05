# -*- coding: utf-8 -*-
from scrapy import Spider, FormRequest, Request
from urllib.parse import urlencode
import json
from time import sleep
import random
from lagou.items import LagouItem


class LagouSpiderSpider(Spider):
    name = 'lagou_spider'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    query_string = {
        'px': 'default',
        'city': '成都',
        'needAddtionalResult': 'false'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.75Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    url_json = 'http://www.lagou.com/jobs/positionAjax.json?'
    url_referer = 'https://www.lagou.com/jobs/list_python?'
    url_referer = url_referer + urlencode(query_string)
    url_json = url_json + urlencode(query_string)

    def start_requests(self):

        headers = self.headers.copy()
        headers['Referer'] = self.url_referer
        for i in range(1, 31):
            form_data = {
                'pn': str(i),
                'kd': 'python'
            }
            yield FormRequest(url=self.url_json, headers=headers, formdata=form_data, callback=self.get_id)

    def get_id(self, response):
        headers = self.headers.copy()
        headers['Referer'] = self.url_referer
        content = json.loads(response.text)
        for i in range(15):
            id = content['content']['positionResult']['result'][i]['positionId']
            url = 'https://www.lagou.com/jobs/'+str(id)+'.html'
            sleep(random.random())
            yield Request(url, headers=headers, callback=self.parse_job)

    def parse_job(self, response):
        item = LagouItem()
        lis = response.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span')
        list = []
        for li in lis:
            list.append(li.xpath('./text()').extract_first())
        item['url'] = response.url
        item['company'] = response.css('div.position-head div.position-content-l div.company::text').extract_first()
        item['job_name'] = response.css('div.position-head div.position-content-l > div > span::text').extract_first()
        item['job_request'] = ''.join(list)
        item['advantage'] = response.css('#job_detail > dd.job-advantage > p::text').extract_first()
        describe = response.css('#job_detail > dd.job_bt > div > p::text').extract()
        item['describe'] = '\n'.join(describe).strip('\xa0')
        address = response.css('#job_detail > dd.job-address.clearfix > div.work_addr > a::text').extract()[:-1]
        #detail = response.xpath('//*[@id="job_detail"]/dd[3]/div[1]/text()').extract_first()
        item['location'] = ''.join(address)
        yield item
