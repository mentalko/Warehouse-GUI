#https://flask-russian-docs.readthedocs.io/ru/latest/patterns/sqlalchemy.html

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()
engine = create_engine("sqlite:///warehouse.db", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
# product_ca = Table('post_tags',
#                      db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
#                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
#                      )
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
"""
    for n, name in enumerate(['First', 'Second', 'Third']):
        p = Product(name=name, count=n)
        session.add(p)
        session.commit()"""

# date = relationship('Date', secondary=Warehouse, backref=backref('product', lazy='dynamic'))


# def create_db():
#     try:
#         db.create_all()
#         for name in ['First', 'Second', 'Third']:
#             p = Post(title= name+' post name', body='some text for {} post'.format(name))
#             db.session.add(p)
#         db.session.commit()
#     except sqlalchemy.exc.IntegrityError:
#         print("ERROR")
#
#
# create_db()


# >>> from models import Post
# >>> post = Post.query.all()
# >>> post
# [<Post id: 1, title: First post name>, <Post id: 2, title: Second post name>, <Post id: 3, title: Third post name>]
# >>> ps = Post.query.filter(Post.title.contains('post'))
# >>> ps.all()
# [<Post id: 1, title: First post name>, ....
# >>> ps = Post.query.filter(Post.title.contains('first'))
# >>> ps.all()
# [<Post id: 1, title: First post name>]
