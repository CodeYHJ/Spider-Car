import scrapy


class SohuCarSpider(scrapy.Spider):
    name = "sohu_cars"

    def start_requests(self):
        urls = [
            'http://db.auto.sohu.com/home'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            ul = response.css('ul.tree')
            lis = ul.css('li.close_child')
            for li in lis:
                brand_tit_a_element = li.css('.brand_tit > a::text').getall()
                brand_id = li.css('.brand_tit > a::attr(id)').get()
                if brand_tit_a_element:
                    brand_tit = brand_tit_a_element[1].replace('\r\n', '').strip()

        except Exception as e:
            print(e)