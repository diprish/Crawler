# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from amazon.books import Books
from scrapy.selector import Selector


class AmazonBooksSpider(CrawlSpider):
    name = "amazon_books"
    allowed_domains = ["amazon.in"]
    start_urls = (
        # "http://www.amazon.in/b?ie=UTF8&node=4149761031",
        # "http://www.amazon.in/b?ie=UTF8&node=4149761031",
        'http://www.amazon.in/Books/b?ie=UTF8&node=976389031',
    )

    rules = [
        # Getting links from base page of Books section
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="acs-tiles-row"]//ul/li',)), callback="follow_leaves",
             follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="mainResults"]/div/h3[@class="newaps"]/a',)),
             callback="parse_page", follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="bottomBar"]/div[@id="pagn"]/span[@class="pagnLink"]/a',)),
             callback="follow_leaves", follow=True),
        Rule(LinkExtractor(restrict_xpaths=(
            '//div[@id="center"]//div[@class="s-item-container"]//div[@class="a-row a-spacing-small"]/a',)),
             callback="parse_secondary_page", follow=True),
    ]

    def parse_page(self, response):
        self.log("primary:page")
        item = Books()
        item["title"] = response.xpath(
            '//div[@id="booksTitle"]//h1[@id="title"]/span[@id="productTitle"]/text()').extract()
        item["url"] = response.url
        return item

    def parse_secondary_page(self, response):
        self.log("secondary:page")
        item = Books()

        # Fetching Header level details
        item["title"] = response.xpath(
            '//div[@class="a-container"]//h1[@id="title"]/span[@id="productTitle"]/text()').extract()

        sub_titles = response.xpath(
            '//div[@class="a-container"]//h1[@id="title"]/span[@class="a-size-medium a-color-secondary a-text-normal"]/text()').extract()
        item["subTitle"] = sub_titles

        # Fetching Authors list
        item["author"] = response.xpath(
            '//div[@class="a-container"]//div[@id="booksTitle"]//div[@id="byline"]/span[@class="author notFaded"]/a[@class="a-link-normal"]/text()').extract()
        item["contribution"] = response.xpath(
            '//div[@class="a-container"]//div[@id="booksTitle"]//div[@id="byline"]/span[@class="author notFaded"]/span[@class="contribution"]/span/text()').extract()

        # Fetching Price
        item["price"] = response.xpath(
            '//div[@class="a-box-inner"]//div[@id="buyNewSection"]//span[@class="a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P"]/text()').extract()

        price_details = \
            response.xpath('//div[@class="a-box-inner"]//div[@id="buyNewInner"]//div[@id="buyBoxInner"]//ul/li')
        temp_list = []
        count = 0
        # for price_item in price_details:
        column_text = response.xpath(
            '//div[@class="a-box-inner"]//div[@id="buyNewInner"]//div[@id="buyBoxInner"]//ul/li//span[@class="a-color-secondary"]/text()').extract()[
            0]
        column_value = response.xpath(
            '//div[@class="a-box-inner"]//div[@id="buyNewInner"]//div[@id="buyBoxInner"]//ul/li//span[@class="a-color-secondary a-text-strike"]/text()').extract()[
            0]
        temp_list.append(column_text)
        temp_list.append(column_value)
        item["mrp"] = temp_list

        price_details = \
            response.xpath('//div[@class="a-box-inner"]//div[@id="buyNewInner"]//div[@id="buyBoxInner"]//ul/li')
        for price_item in price_details:
            local_value = price_item.xpath('//span[@class="a-size-base a-color-secondary"]/text()').extract()
        item["sale"] = local_value

        item["inStock"] = response.xpath('//div[@class="a-box-inner"]//div[@id="availability"]/span/text()').extract()

        # Seller and packing details [Gift wrap]
        item["giftWrapAvailable"] = \
            response.xpath('//div[@class="a-box-inner"]//div[@id="merchant-info"]/text()').extract()[4]
        # Fetching product description
        product_descriptions = response.xpath(
            '//div[@id="pdIframeContent"]/div[@id="productDescription"]//div[@class="content"]')
        product_description_list = []
        for product_description in product_descriptions:
            local_description = product_description.xpath('//h3/text()').extract()
            local_description += '::'
            local_description += product_description.xpath('//div/text()').extract()
            product_description_list.append(local_description)
        item["bookDescription"] = product_description_list

        # Fetching product details
        item["productDetailsLabel"] = response.selector.xpath(
            '//div[@id="detail_bullets_id"]//div[@class="content"]/ul/li/b/text()').extract()

        # Customer Reviews
        item["customerReviewsNo"] = response.xpath(
            '//div[@id="averageCustomerReviews"]/a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract()
        item["rating"] = response.xpath('//div[@id="averageCustomerReviews"]/span[@id="acrPopover"]/@title').extract()

        local_product_details_value = []

        for i in range(len(item["productDetailsLabel"])):
            if i == 6:
                value = response.selector.xpath(
                    '//div[@id="detail_bullets_id"]//div[@class="content"]/ul/li/span/span/a/span/span/text()').extract()[
                    0]
            else:
                value = \
                    response.selector.xpath(
                        '//div[@id="detail_bullets_id"]//div[@class="content"]/ul/li/text()').extract()[
                        i]
                if i == 7:
                    if not self.has_numbers(value):
                        for j in range(1, 100, 1):
                            value = response.selector.xpath(
                                '//div[@id="detail_bullets_id"]//div[@class="content"]/ul/li/text()').extract()[i + j]
                            if self.has_numbers(value):
                                break
            local_product_details_value.append(value)

        item["productDetailsValue"] = local_product_details_value

        item["url"] = response.url
        return item

    def follow_leaves(self, response):
        self.log("LEAF")
        self.log("***********************")
        self.log(response.xpath('//h1/b/text()').extract())
        self.log(response.url)

    def has_numbers(self, input_string):
        return any(char.isdigit() for char in input_string)