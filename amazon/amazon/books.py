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
    contribution = scrapy.Field()
    stars = scrapy.Field()
    customerReviewsNo = scrapy.Field()
    bookDescription = scrapy.Field()
    aboutTheAuthor = scrapy.Field()
    productDetailsLabel = scrapy.Field()
    productDetailsValue = scrapy.Field()
    review = scrapy.Field()
    # mrp
    mrp = scrapy.Field()
    price = scrapy.Field()
    sale = scrapy.Field()
    inStock = scrapy.Field()
    giftWrapAvailable = scrapy.Field()