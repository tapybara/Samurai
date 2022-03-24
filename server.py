############################################## 
# HTTPサーバーの構築
#  Raspberry PiブラウザからLED操作
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
history = History()

def getLedstatus():
    """Read out the LED current status"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.IN)
    signal = GPIO.input(LED_PIN)
    if(signal==1):
        text="ON"
    else:
        text="OFF"
    return text

def ledControl(param):
    """Controlling LED with browser POST communication"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    if(param == "ON"):
        signal = 1
    else:
        signal = 0
    GPIO.output(LED_PIN, signal)
    text = f'LEDが{param}されました'
    lineNotify(text)
    return param

def toDicts_fromBytes(bytes_data):
    """Change Bytes_Data to dicts_data"""
    str_data = bytes_data.decode('utf-8')   #データをstr型に変換
    list_data = str_data.split('=')         #データをリスト型に変換
    return {list_data[0]:list_data[1]}      #データを辞書型に変換

def add_history_info(model, id, user, refer, param_dict):
    """Preparation registration post-datas for history DB"""
    model.user_id = id
    model.user = user
    model.refer = refer
    model.time = datetime.datetime.now()
    model.param = param_dict["params"]

class MyHTTPReqHandler(BaseHTTPRequestHandler):
    """Processing when GET&POST communication is executed"""
    def do_GET(self):
        cwd = os.getcwd()
        if self.path == "/":
            self.path = cwd + "/index.html"
        try:
            split_path = os.path.splitext(self.path)
            request_extension = split_path[1]
            if request_extension != ".py":
                with open(self.path, mode="r", encoding="utf-8") as f:
                    file = f.read()
                db = session.query(History).order_by(desc(history.time)).limit(20).all() #DB(history)から最新アクセスから20個分のデータを取得
                for row in db:
                    print(row.user_id)  #ユーザID
                    print(row.user)     #ユーザ名

                self.send_response(200)
                self.end_headers()
                if (request_extension == '.html'):
                    file = file.replace('{LED}',getLedstatus())

                self.wfile.write(file.encode())
            else:
                f = "File not found"
                print(f'{self.path}が見つかりませんでした。')
                self.send_error(404,f)
        except:
            f = "File not found"
            print(f'{self.path}が見つかりませんでした。')
            self.send_error(404,f)

    def do_POST(self):
        self.send_response(200) #POSTリクエストの受信成功を返答（ターミナルにも記載）
        nbyteslength = self.headers.get('content-length') #ヘッダーからボディーのデータ数を抽出
        param_bytes = self.rfile.read(int(nbyteslength))       #ボディーのデータ(Bytes型)を抽出
        param_dict = toDicts_fromBytes(param_bytes)
        
        #Databaseへの情報登録
        add_history_info(history, 0, "takahito.okuyama", "Mac", param_dict)
        session.add(history)
        session.commit()

        #LEDのON/OFF操作
        ledControl(param_dict["params"])
        self.send_header("Access-Control-Allow-Origin", '*')
        self.end_headers()

if __name__ == "__main__":
    server = HTTPServer((ip, port), MyHTTPReqHandler)
    print("---start web http-_server by Python---")
    server.serve_forever()