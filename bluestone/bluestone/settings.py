# -*- coding: utf-8 -*-

# Scrapy settings for bluestone project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bluestone'

SPIDER_MODULES = ['bluestone.spiders']
NEWSPIDER_MODULE = 'bluestone.spiders'
ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
IMAGES_STORE = 'C:/Crawler/bluestone'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bluestone (+http://www.yourdomain.com)'
