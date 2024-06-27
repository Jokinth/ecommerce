from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:2004@localhost:3306/ecommerce")

local_session = sessionmaker( autoflush=False , bind=engine )

Base = declarative_base()