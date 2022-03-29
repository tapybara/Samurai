import os
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

dialect = "mysql"                       #DBの種類指定
#driver = "mysqldb"                     #DBに接続するためのドライバー指定：指定なし＝"default" DBAPI
username = os.getenv("DB_USER")         #DBへの接続可能なユーザ名
password = os.getenv("DB_PASS")  #DBに接続するためのパスワード
host = "localhost"                      #ホスト名の指定：localhost, IPアドレス等
#port = "3306"                          #ポート指定
database = "LED_CONTROL_DB"             #接続するDBの名の指定
charset_type = "utf8"                   #文字コードの指定

db_url = f"{dialect}://{username}:{password}@{host}/{database}?charset={charset_type}"
ENGINE = create_engine(db_url, echo=True)

# Sessionの作成
# ORM実行時の設定。自動コミットするか、自動反映するなど。
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=ENGINE) # True = 実行毎にSQLを出力
)

Base = declarative_base()
# 予めテーブル定義の継承元クラスにqueryプロパティを仕込んでおく
Base.query = session.query_property()