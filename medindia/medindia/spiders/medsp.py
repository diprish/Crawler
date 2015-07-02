# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from medindia.items import MedindiaItem

class MedspSpider(scrapy.Spider):
    name = "medsp1"
    allowed_domains = ["medindia.net"]
    start_urls = (
        'http://www.medindia.net/drug-price/brand-index.asp',
    )

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="alphabet clear-fix"]/a',)), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//table[@class="content-table"]//td/a',)),
             callback="parse_page", follow=True),
    )

    def parse_page(self, response):
        items = []
        top_right_panel_sel = response.xpath('//div[@id="details-top-right-inner"]')
        item = MedindiaItem()
        item["url"] = response.url
