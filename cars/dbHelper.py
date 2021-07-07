from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings
from cars.modules import db_connect, create_company_table


class DBHelper():
    def __init__(self):
        self.settings = get_project_settings()

    def db_connect(db_url):
        engine = db_connect(db_url)
        create_company_table(engine)
        return sessionmaker(bind=engine)()