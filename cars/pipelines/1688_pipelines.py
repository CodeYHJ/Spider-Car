# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy.orm import sessionmaker

from cars.items import CarItem, FactoryItem, FactorySalesItem, CarSalesItem
from cars.modules import db_connect, create_company_table, Car, Factory, FactorySales, CarSales
from cars.util import Log


class CarsPipeline(object):
    def __init__(self, db_url):
        engine = db_connect(db_url)
        create_company_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.log = Log.createLog('1688_pipelines_log')

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('PG_URL'))

    def close_spider(self):
        self.Session().close()

    def process_item(self, item, spider):
        try:
            session = self.Session()
            if isinstance(item, CarItem):
                car = Car(**item)
                name = item['name']
                sql_data = session.query(Car).filter(Car.name == name).first()
                if sql_data is None:
                    session.add(car)
                    session.commit()
                # else:
                #     sql_data.name = item['name']
                #     sql_data.level = item['level']
                #     sql_data.update_at = item['update_at']
                #     sql_data.car_id = item['car_id']
                #     sql_data.mid = item['mid']
                #     session.commit()
            # elif isinstance(item, SalesItem):
                # mid = item['mid']
                # sql_cars_data = session.query(Cars).filter(Cars.mid == mid).first()
                # if sql_cars_data:
                #     sql_seals_data = session.query(Sales).filter(
                #         and_(Sales.car_id == sql_cars_data.id, Sales.sales_time == item['sales_time'])).first()
                #     if sql_seals_data is None:
                #         sales = Sales(
                #             **{'sales_time': item['sales_time'], 'sales': item['sales'], 'update_at': item['update_at'],
                #                'car_id': sql_cars_data.id})
                #         session.add(sales)
                #         session.commit()
                #     else:
                #         sql_sales_data = session.query(Sales).filter(Car.mid == mid).first()
                #         sql_sales_data.sales_time = item['sales_time']
                #         sql_sales_data.sales = item['sales']
                #         sql_sales_data.update_at = item['update_at']
                #         sql_sales_data.car_id = sql_cars_data.id
                #         session.commit()
            elif isinstance(item, FactoryItem):
                factory = Factory(**item)
                name = item['name']
                sql_data = session.query(Factory).filter(Factory.name == name).first()
                if sql_data is None:
                    session.add(factory)
                    session.commit()
                else:
                    sql_data.name = item['name']
                    sql_data.factory_id = item['factory_id']
                    sql_data.update_at = item['update_at']
                    sql_data.sales_total = item['sales_total']
                    session.commit()
            elif isinstance(item, FactorySalesItem):
                factory_sales = FactorySales(**item)
                sales_date = item['sales_date']
                factory_id = item['factory_id']
                sql_data = session.query(FactorySales).filter(FactorySales.sales_date == sales_date, FactorySales.factory_id == int(factory_id)).first()
                if sql_data is None:
                    session.add(factory_sales)
                    session.commit()
                else:
                    sql_data.sales_num = item['sales_num']
                    sql_data.update_at = item['update_at']
                    session.commit()
            elif isinstance(item, CarSalesItem):
                carSales = CarSales(**item)
                sales_date = item['sales_date']
                factory_id = item['factory_id']
                sql_data = session.query(CarSales).filter(CarSales.sales_date == sales_date, CarSales.factory_id == int(factory_id)).first()
                if sql_data is None:
                    session.add(carSales)
                    session.commit()
                else:
                    sql_data.sales_num = item['sales_num']
                    sql_data.update_at = item['update_at']
                    session.commit()
            return item
        except Exception as e:
            self.log.warning(e)
            self.Session().rollback()

