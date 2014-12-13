# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # Stores Model Name
    model = scrapy.Field()
    # Manufacturer
    manufacturer = scrapy.Field()
    # Reviews
    noOfCustomerReviews = scrapy.Field()
    answeredQuestions = scrapy.Field()
    # mrp
    mrp = scrapy.Field()
    price = scrapy.Field()
    sale = scrapy.Field()
    youSave = scrapy.Field()
    deliveryCharges = scrapy.Field()
    codEligible = scrapy.Field()
    emiAvailable = scrapy.Field()
    inStock = scrapy.Field()
    soldBy = scrapy.Field()
    giftWrapAvailable = scrapy.Field()
    productSummary = scrapy.Field()
    additionalComments = scrapy.Field()
    fullProductInfo = scrapy.Field()
    techDetails = scrapy.Field()
    value = scrapy.Field()
    url = scrapy.Field()
    specialOffer = scrapy.Field()
    imageUrl = scrapy.Field()