# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from amazon.items import AmazonItem
import scrapy

class Amazon1Spider(CrawlSpider):
    name = "amazon3"
    allowed_domains = ["amazon.in"]
    start_urls = ['http://www.amazon.in/s/ref=s9_hps_bw_clnk?node=4348234031&lo=stripbooks&suppress-ve=1&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=merchandised-search-7&pf_rd_t=101&pf_rd_p=537170487&pf_rd_i=976389031']
    rules = [
        Rule(LinkExtractor(restrict_xpaths=('//h3[@class="newaps"]/a',)), callback='parse_page1', follow= True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="bottomBar"]/div[@id="pagn"]/span[@class="pagnLink"]/a',)), follow= True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="a-row a-spacing-small"]/a[@class="a-link-normal s-access-detail-page a-text-normal"]',)), callback='parse_page1', follow= True),
    ]

    def parse_page1(self, response):
        self.log('This is item page! %s' % response.url)
        
        specList = response.xpath('//div[@id="divsinglecolumnminwidth"]')
 
        items = []
        for spec in specList:
            item = AmazonItem()
            item ["title"] = spec.select('//h1[@class="parseasinTitle"]/span[@id="btAsinTitle"]/span/text()').extract()
            #item ["author"] = spec.select('//div[@class="buying"]/span').extract()
            #item ["priceContent"] = spec.select('//td[@id="actualPriceContent"]/span').extract()
            #item ["url"] = response.url
            items.append(item)
        return(items)