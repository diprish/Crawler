# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from amazon.items import AmazonItem


class AmazonSpiderSpider(CrawlSpider):
    name = "amazon_spider"
    allowed_domains = ["www.amazon.in"]
    start_urls = ['http://www.amazon.in/mobiles-accessories/b/ref=sv_e_1?ie=UTF8&node=1389401031']
    rules = (Rule (LxmlLinkExtractor(restrict_xpaths=('//div[@class="asinTextBlock"]/ul/li/a',))
               , callback="parse_items", follow= True),)

    def parse_items(self, response):
        print ('*** response:', response.url)
        hxs = HtmlXPathSelector(response)
        specifications = hxs.select('//h3[@class="newaps"]/a')
        items = []
        for spec in specifications:
            
            item = AmazonItem()
            item ["title"] = spec.select('//span[@class="lrg bold"]/text()').extract()
            print ('**parse_items:', item["title"])
            items.append(item)
        return(items)