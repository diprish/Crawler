# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from amazon.items import AmazonItem

class Amazon1Spider(CrawlSpider):
    name = "amazon1"
    allowed_domains = ["amazon.in"]
    start_urls = ['http://www.amazon.in/smartphones-basic-mobiles/b?ie=UTF8&node=1389432031']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="bottomBar"]/div[@id="pagn"]/span[@class="pagnLink"]/a',))
               , callback='parse_item', follow= True),

    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        specList = response.xpath('//h3[@class="newaps"]/a/span[@class="lrg bold"]')
        
        if not specList:
            specList = response.xpath('//div[@class="s-item-container"]//h2[@class="a-size-base s-inline s-access-title a-text-normal"]')
        
        items = []
        for spec in specList:
            item = AmazonItem()
            item ["title"] = spec.select('text()').extract()
            item["url"] = response.url
            items.append(item)
        return(items)