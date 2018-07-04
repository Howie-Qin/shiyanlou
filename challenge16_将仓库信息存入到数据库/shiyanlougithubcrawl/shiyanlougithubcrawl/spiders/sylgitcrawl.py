#-*- coding: utf-8 -*-
import scrapy
from shiyanlougithubcrawl.items import ShiyanlougithubcrawlItem

class SylgitcrawlSpider(scrapy.Spider):
    name = 'sylgitcrawl'
   # allowed_domains = ['shiyanlougithubcrawl.com']
   #start_urls = ['http://shiyanlougithubcrawl.com/']
    
    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,5))

    def parse(self, response):
        for repository in response.css('li.public'):
            item = ShiyanlougithubcrawlItem({
                'name': repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)"),
                'update_time': repository.xpath('.//relative-time/@datetime').extract_first()
                })
            yield item
            
