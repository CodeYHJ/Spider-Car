import json
import scrapy
import time
from datetime import datetime
from cars.items import FactoryItem, FactorySalesItem

class FactorySpider(scrapy.Spider):
    name = "1688_factory"
    base_url = 'https://xl.16888.com'

    def start_requests(self):
        urls = [
            'https://xl.16888.com/factory.html'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
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
                yield scrapy.Request(url=self.base_url+'/f/'+factory_id+'/', callback=self.parse_factory_sales, cb_kwargs={'factory_id': factory_id})
            if next_page_href:
                url = self.base_url + next_page_href
                yield scrapy.Request(url=url, callback=self.parse)
        except Exception as e:
            print(e)

    def parse_factory_sales(self, response, factory_id):
        try:
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
                # item['sales_date'] = sales_date
                item['sales_date'] = datetime.strptime(sales_date, '%Y-%m').date()
                item['sales_num'] = sales_num
                item['factory_id'] = factory_id
                item['update_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield item
            if next_page_href:
                url = self.base_url + next_page_href
                yield scrapy.Request(url=url, callback=self.parse_factory_sales, cb_kwargs={'factory_id': factory_id})
        except Exception as e:
            print(e)