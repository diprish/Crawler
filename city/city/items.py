# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityItem(scrapy.Item):
    location = scrapy.Field()
    pincode = scrapy.Field()
    state = scrapy.Field()
    district = scrapy.Field()
    pass
