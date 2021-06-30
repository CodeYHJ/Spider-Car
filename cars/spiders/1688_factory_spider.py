import json
import scrapy
import time
from datetime import datetime
from cars.items import FactoryItem, FactorySalesItem, CarItem
from enum import Enum
from enum import unique


@unique
class CarModal(Enum):
    MICRO = 1  # 微型
    SUB_COMPACT = 2  # 小型车
    COMPACT = 3  # 紧凑型
    MID_SIZE = 4  # 中型车
    FULL_SIZE = 5  # 中大型
    MPV = 6
    SUV = 7


class FactorySpider(scrapy.Spider):
    name = "1688_factory"
    base_url = 'https://xl.16888.com'
    custom_settings = {
        'ITEM_PIPELINES': {
            'cars.pipelines.1688_pipelines.CarsPipeline': 400
        }
    }

    def start_requests(self):
        urls = [
            'https://xl.16888.com/factory.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield scrapy.Request(url="https://xl.16888.com/f/57412/history-202104-202104-1.html", callback=self.parse_car)
        try:
            table = response.css("table")
            tr_list = table.css("tr")
            next_page_href = response.css('a.lineBlock.next::attr(href)').get()
            for tr in tr_list:
                td2 = tr.css("td.xl-td-t2")
                if len(td2) == 0:
                    continue
                factory_id = td2.css("a::attr(href)").get().replace('/f/', '').replace('/', '')
                name = td2.css("a::text").get()
                if name is None:
                    continue
                td3_list = tr.css("td.xl-td-t3::text")
                sales_total = td3_list[0].get()
                item = FactoryItem()
                item['name'] = name
                item['sales_total'] = sales_total
                item['factory_id'] = factory_id
                item['update_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield item
                yield scrapy.Request(url=self.base_url + '/f/' + factory_id + '/', callback=self.parse_factory_sales,
                                     cb_kwargs={'factory_id': factory_id})
            if next_page_href:
                url = self.base_url + next_page_href
                yield scrapy.Request(url=url, callback=self.parse)
        except Exception as e:
            print(e)

    def parse_factory_sales(self, response, factory_id):
        try:
            factory_id = factory_id
            table = response.css("table")
            tr_list = table.css("tr")
            next_page_href = response.css('a.lineBlock.next::attr(href)').get()
            for tr in tr_list:
                td4 = tr.css("td.xl-td-t4::text")
                if len(td4) == 0:
                    continue
                sales_date = td4[0].get()
                sales_num = td4[1].get()
                item = FactorySalesItem()
                item['sales_date'] = datetime.strptime(sales_date, '%Y-%m').date()
                item['sales_num'] = sales_num
                item['factory_id'] = factory_id
                item['update_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield item
                car_url_month = self.base_url + '/f/' + factory_id + '/history-' + sales_date.replace('-',
                                                                                                      '') + '-' + sales_date.replace(
                    '-', '') + '-1.html'
                yield scrapy.Request(url=car_url_month, callback=self.parse_car, cb_kwargs={'factory_id': factory_id})
            if next_page_href:
                url = self.base_url + next_page_href
                yield scrapy.Request(url=url, callback=self.parse_factory_sales, cb_kwargs={'factory_id': factory_id})
        except Exception as e:
            print(e)

    def parse_car(self, response, factory_id):
        try:
            table = response.css("table")
            tr_list = table.css("tr")
            for tr in tr_list:
                td4 = tr.css("td.xl-td-t4::text")
                if len(td4) == 0:
                    continue
                td_list = tr.css("td")
                car_id = td_list[0].css("a::attr(href)").get().replace('/s/', '').replace('/', '')
                name = td_list[0].css("a::text").get()
                level_text = td_list[2].css("::text").get()
                level_obj = {
                    "微型车": "MICRO",
                    "小型车": "SUB_COMPACT",
                    "紧凑型车": "COMPACT",
                    "中型车": "MID_SIZE",
                    "中大型车": "FULL_SIZE",
                    "SUV": "SUV",
                    "MPV": "MPV"
                }
                level = CarModal[level_obj[level_text]].value
                item = CarItem()
                item['car_id'] = car_id
                item['name'] = name
                item['level'] = level
                item['factory_id'] = factory_id
                item['update_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield item
        except Exception as e:
            print(e)
