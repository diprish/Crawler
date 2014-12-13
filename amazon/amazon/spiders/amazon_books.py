# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from amazon.books import Books


class AmazonBooksSpider(CrawlSpider):
    name = "amazon_books"
    allowed_domains = ["amazon.in"]
    start_urls = (
        'http://www.amazon.in/Books/b/ref=nav_shopall_books_all?ie=UTF8&node=976389031',
    )

    rules = [
        # Getting links from base page of Books section
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="acs-tiles-row"]//ul/li',)), callback="follow_leaves",
             follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="mainResults"]/div/h3[@class="newaps"]/a',)),
             callback="parse_page", follow=True),
        # Opening the  show all links from base page of Books section
        # Rule(LinkExtractor(
        # restrict_xpaths=('//div[@class="acs-tiles-row"]//div[@class="acs-category-tile-shopall "]/a',)),
        # follow=True),
        # # Checking show all links in 1st leaf level pages
        # Rule(LinkExtractor(
        #     restrict_xpaths=('//div[@class="action"]/a',)), follow=True),
        # Rule(LinkExtractor(restrict_xpaths=('//div[@class="zg_itemWrapper"]/div[@class="zg_title"]/a',)),
        #      callback="parse_page", follow=True),
    ]

    def parse_page(self, response):
        # speclist = response.xpath('//div[@id="a-page"]')
        # #
        # items = []
        # for spec in speclist:
        #     item = AmazonItem()
        #     # item["model"] = spec.select('//h1[@id="title"]/span[@id="productTitle"]/text()').extract()
        #     item["url"] = response.url
        #     items.append(item)
        item = Books()
        item["title"] = response.xpath('//div[@id="booksTitle"]//h1[@id="title"]/span[@id="productTitle"]/text()').extract()
        item["url"] = response.url
        return item

    def follow_leaves(self, response):
        self.log("LEAF")
        self.log("***********************")
        self.log(response.xpath('//h1/b/text()').extract())
        self.log(response.url)
