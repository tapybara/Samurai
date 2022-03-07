############################################## 
# Webサーバの構築
# ver1.1.0： GET/POSTの基本機能（href/drc属性:適用ver）
#           Raspberry PiブラウザからLED操作
############################################## 
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from time import sleep
import os
from urllib import request
import RPi.GPIO as GPIO
from time import sleep

from linenotify import lineNotify

ip = '0.0.0.0'
port = 8080
url = "http://"+ip+":"+str(port);
LED_PIN = 21

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
    lineNotify(param)
    return param
        
class MyHTTPReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/home/pi/Documents/Samurai/localserver_LED_control/index.html"
        try:
            split_path = os.path.splitext(self.path)
            request_extension = split_path[1]
            if request_extension != ".py":
                with open(self.path, mode="r", encoding="utf-8") as f:
                    file = f.read()
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
        length = self.headers.get('content-length') #ヘッダーからボディーのデータ数を抽出
        nbytes = int(length)                        #ボディーのデータ数を整数型に変換
        param_bytes = self.rfile.read(nbytes)       #ボディーのデータ(Bytes型)を抽出
        param_str = param_bytes.decode('utf-8')     #データをstr型に変換
        param_list = param_str.split('=')           #データをリスト型に変換
        param_dict = {param_list[0]:param_list[1]}  #データを辞書型に変換
        
        #関数ledcontrolの引数にデータを渡す
        text = ledControl(param_dict["params"])
        self.send_header("Access-Control-Allow-Origin", '*')
        self.end_headers()

if __name__ == "__main__":
    server = HTTPServer((ip, port), MyHTTPReqHandler)
    print("---start web server by Python---")
    server.serve_forever()