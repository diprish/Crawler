__author__ = 'dipverma'
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from amazon.items import AmazonItem


class AmazonMobileSpider(CrawlSpider):
    name = "amazon_mobile"
    allowed_domains = ["amazon.in"]
    start_urls = (
        "http://www.amazon.in/mobiles-accessories/b?ie=UTF8&node=1389401031",
    )

    rules = [
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="asinTextBlock"]/ul/li/a',)), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(
            '//div[@id="atfResults"]/ul/li/div[@class="s-item-container"]//a[@class="a-link-normal s-access-detail-page a-text-normal"]',)),
             callback="parse_page", follow=True),
    ]

    def parse_page(self, response):
        self.log('This is item page! %s' % response.url)
        speclist = response.xpath('//div[@id="a-page"]')

        items = []
        for spec in speclist:
            item = AmazonItem()
            item["model"] = spec.select('//h1[@id="title"]/span[@id="productTitle"]/text()').extract()
            item["manufacturer"] = spec.select('//div[@id="brandByline_feature_div"]/div[@class="a-section a-spacing-none"]/a/text()').extract()
            item["noOfCustomerReviews"] = spec.select('//div[@id="averageCustomerReviews"]/a[@id="acrCustomerReviewLink"]/span[@id="acrCustomerReviewText"]/text()').extract()
            item["answeredQuestions"] = spec.select('//div[@id="ask_feature_div"]/span/a[@class="a-link-normal"]/span[@class="a-size-base"]/text()').extract()

            pricelist = []
            pricelist = spec.select('//div[@id="price"]/table[@class="a-lineitem"]/tr/td/text()').extract()
            for priceItem in pricelist:
                print priceItem

            item["emiAvailable"] = spec.select('//div[@id="inemi_feature_div"]/text()').extract()
            item["inStock"] = spec.select('//div[@id="availability_feature_div"]/div[@id="availability"]/span/text()').extract()
            item["soldBy"] = spec.select('//div[@id="availability_feature_div"]/div[@id="merchant-info"]/a/text()').extract()
            item["giftWrapAvailable"] = spec.select('//div[@id="availability_feature_div"]/div[@id="merchant-info"]/text()').extract()[2]
            item["productSummary"] = spec.select('//div[@id="featurebullets_feature_div"]/div[@id="feature-bullets"]/ul[@class="a-vertical a-spacing-none"]/li/span/text()').extract()
            item["additionalComments"] = spec.select('//div[@id="productAlert_feature_div"]/text()').extract()
            productheading = spec.select('//div[@class="aplus"]/h5/text()').extract()
            productdetails = spec.select('//div[@class="aplus"]/p/text()').extract()

            heading = ""
            locallist1 = []
            for i in range(len(productheading)):
                heading = productheading[i]
                heading += "::"
                heading += productdetails[i]
                locallist1.append(heading)

            item["fullProductInfo"] = locallist1
            item["url"] = response.url

            labelcollection = spec.select('//div[@class="wrapper INlocale"]/div[@class="container"]//table//tr/td[@class="label"]/text()').extract()
            valuecollection = spec.select('//div[@class="wrapper INlocale"]/div[@class="container"]//table//tr/td[@class="value"]/text()').extract()

            locallist2 = []
            local = ""

            for j in range(len(labelcollection)):
                local = labelcollection[j]
                local += '::'
                local += valuecollection[j]
                locallist2.append(local)

            item["techDetails"] = locallist2
            
            specialofferlist = []
            specialoffercollection = spec.select('//div[@id="heroQuickPromo_feature_div"]//p/text()')
            localspecial = ""
            for i in range(len(specialoffercollection))

        items.append(item)
        return items