from sqlalchemy import Column, Integer, String, ForeignKey , TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base  # Assuming Base is your SQLAlchemy Base object

class User(Base):
    __tablename__ = 'user'

    uid = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(50) ,unique=False)
    email = Column(String(100),  index=True)
    password = Column(String(150))
    mobile_number = Column(String(15))
    role = Column(String(20))  # Assuming role as string for simplicity
    token = Column(String(100))

    addresses = relationship("Address", back_populates="user" , primaryjoin="User.uid == Address.user_id")
    orders = relationship("Order", back_populates="user" ,primaryjoin="User.uid == Order.uid")
    reviews = relationship("Review", back_populates="user",primaryjoin="User.uid == Review.uid")

class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True, index=True)
    street = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    user_id = Column(Integer, ForeignKey('user.uid'))  # Define foreign key here

    user = relationship("User", back_populates="addresses" , primaryjoin="User.uid == Address.user_id")


class Product(Base):
    __tablename__ = 'product'

    pid = Column(Integer, primary_key=True, autoincrement=True)
    pname = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    quantity_available = Column(Integer, nullable=False)
    category = Column(String(50))
    brand = Column(String(30))
    description = Column(String(250))
    reviews = relationship("Review", back_populates="product",primaryjoin="Product.pid == Review.pid")

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey('user.uid'))
    order_time = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    total_amount = Column(Integer, nullable=False)
    address = Column(String(250), nullable=False)

    user = relationship("User", back_populates="orders",primaryjoin="User.uid == Order.uid")
    
class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_text = Column(String(500))  # Adjust the length as needed
    rating = Column(Integer)
    uid = Column(Integer, ForeignKey('user.uid'))
    pid = Column(Integer, ForeignKey('product.pid'))

    user = relationship("User", back_populates="reviews",primaryjoin="User.uid == Review.uid")
    product = relationship("Product", back_populates="reviews",primaryjoin="Product.pid == Review.pid")
