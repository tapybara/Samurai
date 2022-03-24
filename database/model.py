import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from setting import Base
from setting import ENGINE

class History(Base):
    __tablename__ = 'history'
    user_id = Column('user_id', Integer, primary_key = True)    #ユーザーID
    user = Column('user', String(60), nullable=False)               #ユーザー名
    refer = Column('refer', String(20), nullable=False)             #アクセス元IP
    time = Column('time', DateTime, nullable=False)             #アクセス日時
    param = Column('param', String(5))                             #送信内容（ON/OFF情報）

class User(Base):
    __tablename__ = 'users'
    user_id = Column('user_id', Integer, primary_key = True)    #ユーザーID
    user = Column('user', String(60), nullable=False)               #ユーザー名
    password = Column('password', String(20), nullable=False)       #パスワード
    reg_date = Column('reg_date', DateTime, nullable=False)     #登録日

def main(args):
    Base.metadata.create_all(bind=ENGINE)   #Baseを継承しているテーブル郡の一括作成

if __name__ == "__main__":
    main(sys.argv)