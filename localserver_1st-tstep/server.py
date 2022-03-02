############################################## 
# Webサーバの構築
# ver1.0.0： GET/POSTの基本機能
#           Raspberry PiブラウザからLED操作
############################################## 
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from time import sleep
import RPi.GPIO as GPIO
from time import sleep
#import urllib
#import requests

path_html = "/home/pi/Documents/Samurai/localserver_1st-tstep/index.html"
ip = '0.0.0.0'
port = 8080
url = "http://"+ip+":"+str(port);
LED_PIN = 21

def ledControl(param):
    """Controlling LED with browser POST communication"""
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    if(param == "ON"):
        GPIO.output(LED_PIN, 1)
    else:
        GPIO.output(LED_PIN, 0)
        GPIO.cleanup()
        
class MyHTTPReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open(path_html,mode='r',encoding='utf-8') as f:
            html = f.read()
        self.send_response(200)
        self.send_header("User-Agent","test1")
        self.end_headers()        
        self.wfile.write(html.encode())

    def do_POST(self):
        self.send_response(200) #POSTリクエストの受信成功を返答（ターミナルにも記載）
        length = self.headers.get('content-length') #ヘッダーからボディーのデータ数を抽出
        nbytes = int(length)                        #ボディーのデータ数を整数型に変換
        param_bytes = self.rfile.read(nbytes)       #ボディーのデータ(Bytes型)を抽出
        param_str = param_bytes.decode('utf-8')     #データをstr型に変換
        param_list = param_str.split('=')           #データをリスト型に変換
        param_dict = {param_list[0]:param_list[1]}  #データを辞書型に変換
        print(f'Body-param = {param_dict}です')

        #関数ledcontrolの引数にデータを渡す
        ledControl(param_dict["params"])

        ###URLを解析して処理を行いたい場合に記述（記録用）###
        #qs = urllib.parse.urlparse(url).query   #クエリ文字列をURLより抽出
        #res = urllib.parse.parse_qs(qs)         #クエリ文字列を辞書に変換？

        ###HTTPヘッダーにレスポンスを返す場合に必要（記録用）###
        #self.send_header("User-Agent","test1")
        #self.end_headers()

if __name__ == "__main__":
    server = HTTPServer((ip, port), MyHTTPReqHandler)
    print("---start web server by Python---")
    server.serve_forever()
