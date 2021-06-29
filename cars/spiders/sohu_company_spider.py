import json
import scrapy
import time
from datetime import datetime
from cars.items import CarItem, SalesItem
import string
from urllib.parse import quote


class SohuCompanySpider(scrapy.Spider):
    name = "sohu_company"

    def start_requests(self):
        urls = [
            'https://db.auto.sohu.com/brand_191/salesbrand.shtml'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ul = response.css('div.tree_nav > ul')
        lis = ul.css('li.close_child')
        uls = lis.css('ul.tree_con')

        try:
            for ul in uls:
                a = ul.css('li.con_tit > a::text').getall()
                href = ul.css('li.con_tit > a::attr(href)').get()
                href = quote(href, safe=string.printable)
                company_name = a[1].replace('\r\n', '').strip()
                cars = ul.css('a.model-a')
                for car in cars:
                    text_list = car.css(' ::text').getall()
                    mid = car.css(' ::attr(id)').get().replace('m', '')
                    car_name = text_list[1].replace('\r\n', '').strip()
                    item = CarItem()
                    item['name'] = car_name
                    item['company_name'] = company_name
                    item['update_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item['sohu_url'] = href
                    item['mid'] = mid
                    yield item
                    yield scrapy.Request(
                        url="https://db.auto.sohu.com/api/newSales/model?modelIds={}&section=0".format(mid),
                        callback=self.parse_sales, cb_kwargs={'mid': mid})
        except Exception as e:
            print(e)

    def parse_sales(self, response, mid):
        try:
            data = json.loads(response.text)
            data = data.get('result')
            if data:
                list = data[0].get('salesList')
                for l in list:
                    item = SalesItem()
                    transform_data = l.get('v').replace('年', '-').replace('月', '')
                    item['sales_time'] = datetime.strptime(transform_data, '%Y-%m')
                    item['sales'] = int(float(l.get('y')) * 10000)
                    item['update_at'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item['mid'] = mid
                    yield item
        except Exception as e:
            print(e)
