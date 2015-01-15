# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BluestoneItem(scrapy.Item):
    title = scrapy.Field()
    product_code = scrapy.Field()
    price = scrapy.Field()
    sub_title = scrapy.Field()
    price_breakup = scrapy.Field()
    gold_option = scrapy.Field()
    metal_purity_options = scrapy.Field()
    diamond_quality_options = scrapy.Field()
    line_product_details = scrapy.Field()
    stone_details = scrapy.Field()

    # diamond details
    metal_detail_type = scrapy.Field()

    # metal details
    metal_detail_value = scrapy.Field()
    url = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_details = scrapy.Field()
    image_paths = scrapy.Field()