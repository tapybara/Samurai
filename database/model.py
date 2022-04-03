import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from database.setting import Base
from database.setting import ENGINE

class History(Base):
    __tablename__ = 'history'
    id = Column('id', Integer, primary_key = True)    #ID
    user = Column('user', String(60), nullable=False)           #ユーザー名
    refer =Column('refer', String(20), nullable=False)          #アクセス元デバイス情報
    time = Column('time', DateTime, nullable=False)             #DB登録日時
    param = Column('param', String(5))                          #送信内容（ON/OFF情報）

    def __init__(self, id, user, refer, time, param):
        self.id = id
        self.user = user
        self.refer = refer
        self.time = time
        self.param = param

class User(Base):
    __tablename__ = 'user'
    id = Column('id', Integer, primary_key = True)              #ユーザーID
    user = Column('user', String(60), nullable=False)           #ユーザー名
    password = Column('password', String(20), nullable=False)   #パスワード
    reg_date = Column('reg_date', DateTime, nullable=False)     #登録日
    address = Column('address', String(483), nullable=False)    #住所情報
    phone_num = Column('phone_num', String(21), nullable=False) #電話番号

def main(args):
    Base.metadata.create_all(bind=ENGINE)   #Baseを継承しているテーブル郡の一括作成

if __name__ == "__main__":
    main(sys.argv)