############################################## 
# HTTPサーバーの構築
#  ブラウザからRaspberry Piを操作
#  Frameworkを使用しないGET/POST処理・DB操作
############################################## 
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib import request
from time import sleep
import os
import RPi.GPIO as GPIO
import datetime
from sqlalchemy import desc, asc

from linenotify import lineNotify
from database.setting import session
from database.model import *

ip = '0.0.0.0'
port = 80
url = "http://"+ip+":"+str(port);
LED_PIN = 21

def getLedstatus():
    """Read out the LED current status"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.IN)
    signal = GPIO.input(LED_PIN)
    if(signal==1):
        status="ON"
    else:
        status="OFF"
    return status

def ledControl(param):
    """Controlling LED with browser POST communication"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    if(param == "ON"):
        signal = 1
    else:
        signal = 0
    GPIO.output(LED_PIN, signal)
    comment = f'LEDが{param}されました'
    lineNotify(comment)
    return param

def toDicts_fromBytes(bytes_data):
    """Change Bytes_Data to dicts_data"""
    str_data = bytes_data.decode('utf-8')   #データをstr型に変換
    list_data = str_data.split('=')         #データをリスト型に変換
    return {list_data[0]:list_data[1]}      #データを辞書型に変換

def add_DBinfo(model, id, user, refer, param_dict):
    """Preparation registration post-datas for history DB"""
    model.id = id
    model.user = user
    model.refer = refer
    model.time = datetime.datetime.now()
    model.param = param_dict["params"]
    
def get_DBinfo(model):
    "#DB(model)から最新アクセスから最大10個分のレコードとレコード数を取得"
    records = session.query(model).order_by(desc(model.time)).limit(10).all() 
    return records
    
def generate_tagFromRecord(records):
    "#取得したレコードからHTMLタグを生成"
    text = ""   #HTML生成テキストの初期化
    text += """
    <tr>
    <th>アクセス日時</th>
    <th>ユーザー名</th>
    <th>送信内容</th>
    <th>アクセス元IP</th>
    </tr>
    """
    for record in records:
        text += "<tr>"
        text += "<td>"+str(record.time)+"</td>"
        text += "<td>"+str(record.user)+"</td>"
        text += "<td>"+str(record.param)+"</td>"
        text += "<td>"+str(record.refer)+"</td>"
        text += "</tr>"
    return text
    
class MyHTTPReqHandler(BaseHTTPRequestHandler):
    """Processing when GET&POST communication is executed"""
    def do_GET(self):
        if self.path == "/":
            self.path = "./index.html"
        try:
            split_path = os.path.splitext(self.path)
            request_extension = split_path[1]
            if request_extension != ".py":
                with open("./"+self.path, mode="r", encoding="utf-8") as f:
                    file = f.read()
        except FileNotFoundError:
            print(f'{self.path}が見つかりませんでした。')
            f = "File not found"
            self.send_error(404,f)
        else:
            self.send_response(200)
            self.end_headers()
            if (request_extension == '.html'):
                records = get_DBinfo(History)
                file = file.replace('{database}',generate_tagFromRecord(records))
                file = file.replace('{LED}',getLedstatus())
            self.wfile.write(file.encode())

    def do_POST(self):
        self.send_response(200) #POSTリクエストの受信成功を返答（ターミナルにも記載）
        content_len = int(self.headers.get('content-length'))      #ヘッダーからボディーのデータ数を抽出
        param_bytes = self.rfile.read(content_len)       #ボディーのデータ(Bytes型)を抽出
        param_dict = toDicts_fromBytes(param_bytes)
        
        #Databaseへの情報登録
        history = History()
        add_DBinfo(history, 0, "takahito.okuyama", "Mac", param_dict)
        session.add(history)
        session.commit()

        #LEDのON/OFF操作
        ledControl(param_dict["params"])

        #レスポンス
        self.send_header("Access-Control-Allow-Origin", '*')
        self.end_headers()
        records = get_DBinfo(History)
        text = generate_tagFromRecord(records)
        self.wfile.write(text.encode())

if __name__ == "__main__":
    server = HTTPServer((ip, port), MyHTTPReqHandler)
    print("---start web http-_server by Python---")
    server.serve_forever()