# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Books(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    subTitle = scrapy.Field()
    author = scrapy.Field()
    stars = scrapy.Field()
    customerReviewsNo = scrapy.Field()
    shortDescription = scrapy.Field()
    aboutTheAuthor = scrapy.Field()
    productDetails = scrapy.Field()