import scrapy
from medindia.items import MedindiaItem


class DmozSpider(scrapy.Spider):
    name = "medsp2"
    allowed_domains = ["medindia.net"]
    start_urls = [
        "http://www.medindia.net/drug-price/index.asp",
    ]

    def parse(self, response):
        for href in response.css("table.content-table > tr > td > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_level_1)

    def parse_level_1(self, response):
        for a in response.css("table.content-table > tr > td > a"):
            atext = a.xpath('text()').extract()
            href = a.xpath('@href')
            url = response.urljoin(href.extract()[0])
            yield scrapy.Request(url, callback=self.parse_drug_price)
        pass

    def parse_drug_price(self, response):
        print '**********In child'
        for sel in response.xpath('//table[@class="content-table"]//tr'):
            item = MedindiaItem()
            item['tradeName'] = sel.xpath('td/text()').extract()
            yield item