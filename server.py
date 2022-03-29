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

port = 80
LED_PIN = 21

def getLedStatus():
    """Read out the LED current status"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.IN)
    signal = GPIO.input(LED_PIN)
    if(signal==1):
        return "ON"
    else:
        return "OFF"

def ledControl(param):
    """Controlling LED with browser POST communication"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    if(param == "ON"):
        signal = 1
    else:
        signal = 0
    GPIO.output(LED_PIN, signal)
    lineNotify(f'LEDが{param}されました')
    return param

def toDictsFromByte(bytes_data):
    """Change Bytes_Data to dicts_data"""
    str_data = bytes_data.decode('utf-8')   #データをstr型に変換
    list_data = str_data.split('=')         #データをリスト型に変換
    return {list_data[0]:list_data[1]}      #データを辞書型に変換
    
def generateTagFromRecord(records):
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
                records = session.query(History).order_by(desc(History.time)).limit(10).all() 
                file = file.replace('{database}',generateTagFromRecord(records))
                file = file.replace('{LED}',getLedStatus())
            self.wfile.write(file.encode())

    def do_POST(self):
        self.send_response(200) #POSTリクエストの受信成功を返答（ターミナルにも記載）
        content_len = int(self.headers.get('content-length'))      #ヘッダーからボディーのデータ数を抽出
        param_bytes = self.rfile.read(content_len)       #ボディーのデータ(Bytes型)を抽出
        param_dict = toDictsFromByte(param_bytes)
        
        #Databaseへの情報登録
        history = History(0, "takahito.okuyama", "Mac", datetime.datetime.now(), param_dict["params"])
        session.add(history)
        session.commit()

        #LEDのON/OFF操作
        ledControl(param_dict["params"])

        #レスポンス
        self.send_header("Access-Control-Allow-Origin", '*')
        self.end_headers()
        records = session.query(History).order_by(desc(History.time)).limit(10).all()
        text = generateTagFromRecord(records)
        self.wfile.write(text.encode())

if __name__ == "__main__":
    server = HTTPServer(("", port), MyHTTPReqHandler)
    print("---start web http-_server by Python---")
    server.serve_forever()