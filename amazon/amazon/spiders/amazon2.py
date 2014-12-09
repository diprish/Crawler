# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from amazon.items import AmazonItem
import scrapy

class Amazon1Spider(CrawlSpider):
    name = "amazon2"
    allowed_domains = ["amazon.in"]
    start_urls = ['http://www.amazon.in/smartphones-basic-mobiles/b?ie=UTF8&node=1389432031']
    
    rules = [
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="mainResults"]//h3[@class="newaps"]/a',)), callback='parse_page1', follow= True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="bottomBar"]/div[@id="pagn"]/span[@class="pagnLink"]/a',)), follow= True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="s-item-container"]//a[@class="a-link-normal s-access-detail-page a-text-normal"]',)), callback='parse_page1', follow= True),
    ]

    def parse_page1(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        
        specList = response.xpath('//div[@class="pdTab"]//tr')
 
        items = []
        for spec in specList:
            item = AmazonItem()
            item ["label"] = spec.select('//td[@class="label"]/text()').extract()
            item ["value"] = spec.select('//td[@class="value"]/text()').extract()
            item ["url"] = response.url
            items.append(item)
        return(items)