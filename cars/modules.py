from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()


def db_connect(db_url):
    return create_engine(db_url)


def create_company_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Sales(DeclarativeBase):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sales_time = Column('sales_time', Date)
    sales = Column('sales', Integer)
    update_at = Column('update_at', DateTime)
    car_id = Column('car_id', Integer)


class Cars(DeclarativeBase):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    company_name = Column('company_name', String)
    sohu_url = Column('sohu_url', String)
    update_at = Column('update_at', DateTime)
    mid = Column('mid', Integer)


class Factory(DeclarativeBase):
    __tablename__ = "factory"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    factory_id = Column('factory_id', Integer)
    update_at = Column('update_at', DateTime)


class FactorySales(DeclarativeBase):
    __tablename__ = "factory_sales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sales_num = Column('sales_num', Integer)
    factory_id = Column('factory_id', Integer)
    update_at = Column('update_at', DateTime)
    sales_date = Column('sales_date', DateTime)


class Car(DeclarativeBase):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    level = Column('level', Integer)
    car_id = Column('car_id', Integer)
    factory_id = Column('factory_id', Integer)
    update_at = Column('update_at', DateTime)


class CarSales(DeclarativeBase):
    __tablename__ = "car_sales"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sales_num = Column('sales_num', Integer)
    car_id = Column('car_id', Integer)
    update_at = Column('update_at', DateTime)
    sales_date = Column('sales_date', DateTime)