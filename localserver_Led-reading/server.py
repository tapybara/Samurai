############################################## 
# Webサーバの構築
# ver1.2.0：LEDの状態を読み取ってHTMLに反映
############################################## 
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from telnetlib import STATUS
from urllib import request
import RPi.GPIO as GPIO
from time import sleep
#import urllib
#import requests

path_html = "/home/pi/Documents/Samurai/localserver_Led-reading/index.html"
LED_PIN = 21
ip = '0.0.0.0'
port = 8080
url = "http://"+ip+":"+str(port);

def getLedstatus():
    """Read out the LED current status"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.IN)
    signal = GPIO.input(LED_PIN)
    if(signal==1):
        text="ON"
    else:
        text="OFF"
    return signal, text

def ledControl(param):
    """Controlling LED with browser POST communication"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    if(param == "ON"):
        signal = 1
    else:
        signal = 0
    GPIO.output(LED_PIN, signal)
    return param
        
class MyHTTPReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        signal,text = getLedstatus()
        with open(path_html, mode='r',encoding='utf-8') as f:
            html = f.read()
        body = html.replace('{LED}',text)
        
        self.send_header("User-Agent","test1")
        self.end_headers()
        self.wfile.write(body.encode())

    def do_POST(self):
        self.send_response(200) #POSTリクエストの受信成功を返答（ターミナルにも記載）
        length = self.headers.get('content-length') #ヘッダーからボディーのデータ数を抽出
        nbytes = int(length)                        #ボディーのデータ数を整数型に変換
        param_bytes = self.rfile.read(nbytes)       #ボディーのデータ(Bytes型)を抽出
        param_str = param_bytes.decode('utf-8')     #データをstr型に変換
        param_list = param_str.split('=')           #データをリスト型に変換
        param_dict = {param_list[0]:param_list[1]}  #データを辞書型に変換
        print(f'Body-param = {param_dict}です')

        #LEDをON・OFF制御した後、HTMLにその状態を表示
        #indexを再度読み出して、現在のLEDの点灯状態を反映してレスポンス
        text = ledControl(param_dict["params"])
        with open(path_html, mode='r',encoding='utf-8') as f:
            html = f.read()
        body = html.replace('{LED}',text)
        self.send_header("User-Agent","test1")
        self.end_headers()
        self.wfile.write(body.encode())

if __name__ == "__main__":
    server = HTTPServer((ip, port), MyHTTPReqHandler)
    print("---start web server by Python---")
    server.serve_forever()
