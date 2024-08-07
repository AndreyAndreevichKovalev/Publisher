import os
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, join

from dotenv import load_dotenv


Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=50))
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="book")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"))   # , nullable=False
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"))   # , nullable=False
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sale")

def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

load_dotenv()
DSN = os.getenv("DSN")
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

# # создание объектов
Pb1 = Publisher(name="O\u2019Reilly")
Pb2 = Publisher(name="Pearson")
Pb3 = Publisher(name="Microsoft Press")
Pb4 = Publisher(name="No starch press")

Bk1 = Book(title="Programming Python, 4th Edition", publisher_id=1)
Bk2 = Book(title="Learning Python, 4th Edition", publisher_id=1)
Bk3 = Book(title="Natural Language Processing with Python", publisher_id=1)
Bk4 = Book(title="Hacking: The Art of Exploitation", publisher_id=4)
Bk5 = Book(title="Modern Operating Systems", publisher_id=2)
Bk6 = Book(title="Code Complete: Second Edition", publisher_id=3)

Sh1 = Shop(name="Labirint")
Sh2 = Shop(name="OZON")
Sh3 = Shop(name="Amazon")

St1 = Stock(id_shop=1, id_book=1, count=34)
St2 = Stock(id_shop=1, id_book=2, count=30)
St3 = Stock(id_shop=1, id_book=3, count=0)
St4 = Stock(id_shop=2, id_book=5, count=40)
St5 = Stock(id_shop=2, id_book=6, count=50)
St6 = Stock(id_shop=3, id_book=4, count=10)
St7 = Stock(id_shop=3, id_book=6, count=10)
St8 = Stock(id_shop=2, id_book=1, count=10)
St9 = Stock(id_shop=3, id_book=1, count=10)

Sa1 = Sale(price="50.05", date_sale="2018-10-25T09:45:24.552Z)", id_stock=1, count=16)
Sa2 = Sale(price="50.05", date_sale="2018-10-25T09:51:04.113Z)", id_stock=3, count=10)
Sa3 = Sale(price="10.50", date_sale="2018-10-25T09:52:22.194Z)", id_stock=6, count=9)
Sa4 = Sale(price="16.00", date_sale="2018-10-25T10:59:56.230Z)", id_stock=5, count=5)
Sa5 = Sale(price="16.00", date_sale="2018-10-25T10:59:56.230Z)", id_stock=9, count=5)
Sa6 = Sale(price="16.00", date_sale="2018-10-25T10:59:56.230Z)", id_stock=4, count=1)

session.add_all([Pb1, Pb2, Pb3, Pb4,
                 Bk1, Bk2, Bk3, Bk4, Bk5, Bk6,
                 Sh1, Sh2, Sh3,
                 St1, St2, St3, St4, St5, St6, St7, St8, St9,
                 Sa1, Sa2, Sa3, Sa4, Sa5, Sa6])
session.commit()

def get_Publisher(txt):
    if txt.isdigit():
        q = session.query(
            Book, Shop, Sale, Sale,
        ).select_from(Shop). \
            join(Stock, Stock.id_shop == Shop.id). \
            join(Book, Book.id == Stock.id_book). \
            join(Publisher, Publisher.id == Book.publisher_id). \
            join(Sale, Sale.id_stock == Stock.id). \
            filter(Publisher.id == txt). \
            all()
    else:
        q = session.query(
            Book, Shop, Sale, Sale,
        ).select_from(Shop). \
            join(Stock, Stock.id_shop == Shop.id). \
            join(Book, Book.id == Stock.id_book). \
            join(Publisher, Publisher.id == Book.publisher_id). \
            join(Sale, Sale.id_stock == Stock.id). \
            filter(Publisher.name == txt). \
            all()

    for book, shop, sale, date in q:
        print(f"{book.title: <40} | {shop.name: <10} | {sale.price: <8} | {date.date_sale.strftime('%d-%m-%Y')}")

if __name__ == '__main__':

    txt = input("Введите номер или имя издателя \n(1, 2, 3, 4 или O'Reilly, Pearson, Microsoft Press, No starch press): ")
    print()
    get_Publisher(txt)
