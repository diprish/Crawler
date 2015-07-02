# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from bluestone.items import BluestoneItem


class JewellerySpider(CrawlSpider):
    name = 'jewellery1'
    allowed_domains = ['www.bluestone.com']
    start_urls = ['http://www.bluestone.com/all-jewellery.html?sortby=mostpopular&ref=Menu_AllJewellery', ]
    # "http://www.bluestone.com/jewellery/rings.html?preferredProducts=504,1065,1100,2927,4412,4725&ref=Category_Rings_All",]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="content-column"]//ul/li/a',)), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="animated txt_c v-a-btn"]/li/a',)), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="search-result"]//div[@class="inner"]/a',)),
             callback="parse_page", follow=True),
    )

    def parse_page(self, response):
        items = []
        top_right_panel_sel = response.xpath('//div[@id="details-top-right-inner"]')
        item = BluestoneItem()
        item["url"] = response.url
        for top_right_detail_sel in top_right_panel_sel:
            # Fetching Top Right Panel details
            item["title"] = top_right_detail_sel.xpath('//h1/text()').extract()
            item["product_code"] = top_right_detail_sel.xpath('//div[@id="product-code"]/text()').extract()
            currency = top_right_detail_sel.xpath(
                '//div[@class="price-wrapper"]//span[@class="WebRupee"]/text()').extract()
            price = top_right_detail_sel.xpath(
                '//div[@class="price-wrapper"]//span[@id="our_price_display"]/text()').extract()
            item["price"] = currency + price
            item["sub_title"] = top_right_detail_sel.xpath('//div[@id="short_desc"]/text()').extract()

            # Price Breakup
            price_breakup = []
            price_breakup_sel = top_right_detail_sel.xpath(
                '//div[@id="price-breakup"]//div')
            for price_item_sel in price_breakup_sel:
		price_breakup_list = price_item_sel.xpath('.//text()').extract()
                price_breakup_value = "".join(price_breakup_list)
                price_breakup.append(price_breakup_value)

            item["price_breakup"] = price_breakup

            # Metal Purity
            metal_purity = []
            metal_purity_sel = response.xpath(
                '//div[@id="selectMetalAndDiamondQuality"]//span[@class="White-purities metal-purities"]/label/text()').extract()
            for metal_purity_item_sel in metal_purity_sel:
                white_metal_purity = metal_purity_item_sel
                metal_purity.append(['White', white_metal_purity])

            metal_purity_sel = response.xpath(
                '//div[@id="selectMetalAndDiamondQuality"]//span[@class="Yellow-purities metal-purities"]/label/text()').extract()
            for metal_purity_item_sel in metal_purity_sel:
                yellow_metal_purity = metal_purity_item_sel
                metal_purity.append(['Yellow', yellow_metal_purity])
            item["metal_purity_options"] = metal_purity

            # Diamond Quality
            diamond_quality = []
            diamond_quality_sel = top_right_detail_sel.xpath(
                '//div[@id="selectMetalAndDiamondQuality"]/div//label/input[@name="diamondQuality"]/@value').extract()
            for diamond_quality_item_sel in diamond_quality_sel:
                diamond_quality.append(diamond_quality_item_sel)
            item["diamond_quality_options"] = diamond_quality

        # Fetching line level Product Details
        line_product_details = []
        line_product_details_sel = response.xpath('//section[@id="section-item-details"]//dl')
        for line_product_item_sel in line_product_details_sel:
            key = line_product_item_sel.xpath('./dt/text()').extract()[0]
            value = line_product_item_sel.xpath('./dd/text()').extract()[0]
            line_product_details.append(key + ':' + value)
        item["line_product_details"] = line_product_details

        # Fetching Diamond details
        stone_details = []

        for stone_detail_sel in response.xpath('//section[@id="stone-details"]'):
            stone_name = stone_detail_sel.xpath('./h2[@class="title"]/text()').extract()

            all_content_sel = stone_detail_sel.xpath('./div[@class="content"]//tr')
            all_content = []
            for content_sel in all_content_sel:
                content_title = content_sel.xpath('./td[@class="title"]/text()').extract()[0]
                content_value = content_sel.xpath('./td/text()').extract()[1]
                all_content.append([content_title, content_value])
            stone_details.append([stone_name, all_content])
        item["stone_details"] = stone_details

        # Fetching Metal details
        metal_detail_type = []
        metal_detail_type_sel = response.xpath('//section[@id="metal-details"]//tr/td[@class="title"]/text()').extract()
        for metal_detail_sel in metal_detail_type_sel:
            metal_detail_type.append(metal_detail_sel)
        item["metal_detail_type"] = metal_detail_type

        metal_detail_value = []
        detail_value_sel = response.xpath('//section[@id="metal-details"]//tr/td[@class="last"]')
        for metal_detail_value_sel in detail_value_sel:
            locallist = metal_detail_value_sel.xpath('.//text()').extract()
            localvalue = " ".join(locallist)
            metal_detail_value.append(localvalue)
        item["metal_detail_value"] = metal_detail_value

        # Fetching images
        image_container = []
        image_details = []

        # image_container_sel = response.xpath('//ul[@class="clearfix"]/li/a')
        # for image_object in image_container_sel:
        #     image_title = image_object.xpath('./@title').extract()
        #     image_src = image_object.xpath('./img/@src').extract()
        #     image_alt = image_object.xpath('./img/@alt').extract()
        #     image_big = image_object.xpath('./@href').extract()
        #     image_medium = image_object.xpath('./@rel').extract()[0].split(',')[1].split(':', 1)[1].strip().replace("'",
        #                                                                                                             "").split()
        #     image_container.append(image_big)
        #     image_container.append(image_medium)
        #     print '************'
        #     print image_medium
        #     print image_big
        #     print image_src
        #     image_container.append(image_src)
        #     image_details.append([image_title, image_alt])
        #
        # item["image_details"] = image_details
        # item["image_urls"] = image_container
        # item["image_urls"] = image_container
        items.append(item)
        return items


