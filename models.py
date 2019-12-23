#https://flask-russian-docs.readthedocs.io/ru/latest/patterns/sqlalchemy.html

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()
engine = create_engine("sqlite:///warehouse.db", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    producer = Column(String(100))
    category_id = Column(Integer, ForeignKey('category.id'))
    #
    category = relationship('Category', backref='categories')
    #
    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)

class Warehouse(Base):
    __tablename__ = 'warehouse'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    date = Column(String(20))
    count = Column(Integer)
    #
    product = relationship("Product", backref='products')
    #
    def __init__(self, *args, **kwargs):
        super(Warehouse, self).__init__(*args, **kwargs)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session.commit()

