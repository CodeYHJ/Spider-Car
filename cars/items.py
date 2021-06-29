# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class TutorialItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#
#     pass

class SalesItem(scrapy.Item):
    sales_time = scrapy.Field()
    sales = scrapy.Field()
    update_at = scrapy.Field()
    car_id = scrapy.Field()
    id = scrapy.Field()
    mid = scrapy.Field()


# class CarItem(scrapy.Item):
#     name = scrapy.Field()
#     company_name = scrapy.Field()
#     update_at = scrapy.Field()
#     id = scrapy.Field()
#     sohu_url = scrapy.Field()
#     mid = scrapy.Field()


class FactoryItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    factory_id = scrapy.Field()
    country = scrapy.Field()
    sales_total = scrapy.Field()
    update_at = scrapy.Field()


class FactorySalesItem(scrapy.Item):
    id = scrapy.Field()
    sales_date = scrapy.Field()
    sales_num = scrapy.Field()
    update_at = scrapy.Field()
    factory_id = scrapy.Field()


class CarItem(scrapy.Item):
    update_at = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    level = scrapy.Field()
    car_id = scrapy.Field()
    factory_id = scrapy.Field()
