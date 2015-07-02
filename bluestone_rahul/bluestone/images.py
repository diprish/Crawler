# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class BlueStoneImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url_list in item['image_urls']:
            for image in image_url_list:
                yield scrapy.Request(image)
        # return [Request(x) for x in item.get(self.IMAGES_URLS_FIELD, [])]

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
