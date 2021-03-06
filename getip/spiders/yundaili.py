# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from getip.items import GetipItem


class YundailiSpider(CrawlSpider):
    name = 'yundaili'
    allowed_domains = ['www.ip3366.net']
    start_urls = ['http://www.ip3366.net/free/?stype=1&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.ip3366.net/free/?stype=1&page=(20|1[0-9]|[1-9])$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        table = response.xpath('//div[@id="list"]/table')[0]
        trs = table.xpath('//tr')[1:]  # 去掉标题行
        items = []
        for tr in trs:
            pre_item = GetipItem()
            pre_item['host'] = tr.xpath('td[1]/text()').extract()[0]
            pre_item['port'] = tr.xpath('td[2]/text()').extract()[0]
            pre_item['type'] = tr.xpath('td[4]/text()').extract()[0]
            pre_item['loc'] = tr.xpath('td[5]/text()').extract()[0]
            items.append(pre_item)
        return items