# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from city.items import CityItem


class CitylistSpider(CrawlSpider):
    name = "citylist"
    allowed_domains = ["www.mapsofindia.com"]
    start_urls = (
        'http://www.mapsofindia.com/pincode/india/',
        # 'http://www.mapsofindia.com/pincode/india/madhya-pradesh/',
        # 'http://www.mapsofindia.com/pincode/india/madhya-pradesh/anuppur/achalpur.html',
    )

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="table_hide"]//td/a',)), process_links='process_links',
             callback="parse_page", follow=True),
    )

    def parse_page(self, response):
        self.log("******************")

        item = CityItem()
        try:
            item["location"] = response.xpath('//table[@class="extrtable"]//tr/td/text()').extract()[0]
        except IndexError:
            pass

        try:
            item["pincode"] = response.xpath('//table[@class="extrtable"]//tr/td/b/text()').extract()[4]
        except IndexError:
            pass

        try:
            item["state"] = response.xpath('//table[@class="extrtable"]//tr/td/text()').extract()[1]
        except IndexError:
            pass

        try:
            item["district"] = response.xpath('//table[@class="extrtable"]//tr/td/text()').extract()[2]
        except IndexError:
            pass
        return item

    def process_links(self, links):
        for i, w in enumerate(links):
            w.url = w.url.replace("../", "")
            links[i] = w
        return links