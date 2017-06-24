# -*- coding: utf-8 -*-
import scrapy
from scrape_ukr_forums.items import ScrapeUkrForumsItem
from scrapy.http.response.html import HtmlResponse


class UkrcenterSpider(scrapy.Spider):
    name = 'ukrcenter'
    allowed_domains = ['replace.org.ua']
    start_urls = []
    for i in range(16, 8259):
        start_urls.append('http://replace.org.ua/topic/{}/'.format(i))

    def parse(self, response):
        print('HERE2', response, type(response))
        links = response.xpath('//p[@class="paging"]/a/@href').extract()
        if links:
            yield self.parse_dir_contents(response)
            num = int(sorted(links)[-1].split('/')[-2])
            for j in range(2, num+1):
                # new_r = response.url + 'page/{}/'.format(j)
                # response = HtmlResponse(url=new_r)
                # print('HEREHERE', response, type(response))
                yield scrapy.Request(response.url + 'page/{}/'.format(j),
                                     callback=self.parse_dir_contents)
        else:
            yield self.parse_dir_contents(response)


    def parse_dir_contents(self, response):
        print('HERE3', response)
        item = ScrapeUkrForumsItem()
        item['data'] = response.xpath('//div[@class="entry-content"]/p/text()').extract()
        new = []
        for i in item['data']:
            new.append(i.encode('utf8'))
        return item

