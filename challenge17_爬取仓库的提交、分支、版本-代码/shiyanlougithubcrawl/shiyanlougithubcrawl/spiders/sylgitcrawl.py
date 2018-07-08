# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithubcrawl.items import ShiyanlougithubcrawlItem 

class SylgitcrawlSpider(scrapy.Spider):
    name = 'sylgitcrawl'
   # allowed_domains = ['sylgitcrawl.com']
   # start_urls = ['http://sylgitcrawl.com/']
    
    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1,5))

    def parse(self, response):
        for repository in response.css('li.public'):
            item = ShiyanlougithubcrawlItem()
            item['name'] = repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)")
            item['update_time'] = repository.xpath('.//relative-time/@datetime').extract_first()
            repo_url = response.urljoin(repository.xpath('.//a/@href').extract_first())
            request = scrapy.Request(repo_url, callback=self.parse_repo)
            request.meta['item'] = item
            yield request

    def parse_repo(self, response):
        item = response.meta['item']
        l = response.css('span.num::text').extract()
        if l:
            item['commits'] = l[0].strip()
            item['branches'] = l[1].strip()
            item['releases'] = l[2].strip()
            yield item
        else:
            pass
