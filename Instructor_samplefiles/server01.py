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
# import RPi.GPIO as GPIO
from time import sleep
# import urllib
# import requests

ip = '0.0.0.0'
port = 8080
url = "http://"+ip+":"+str(port)
LED_PIN = 21


def ledControl(param):
    """Controlling LED with browser POST communication"""
#    GPIO.setmode(GPIO.BCM)
#    GPIO.setup(LED_PIN, GPIO.OUT)
#    if(param == "ON"):
#        GPIO.output(LED_PIN, 1)
#    else:
#        GPIO.output(LED_PIN, 0)


class MyHTTPReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        try:
            split_path = os.path.splitext(self.path)
            request_extension = split_path[1]
            if request_extension != ".py":
                print(self.path[1:])
                # Point1: 読み込むときのエンコードを指定する。
                f = open(self.path[1:], encoding='utf-8').read()
                # self.send_header("User-Agent", "test1") # Point2: User-Agentは不要なため削除する。
                # Point3: 読み込みが成功した場合に、HTTP Statusの200を返す。
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.encode())
            else:
                f = "File not found"
                print(f'{self.path}が見つかりませんでした。')
                self.send_error(404, f)
        except:
            f = "File not found"
            print(f'{self.path}が見つかりませんでした。')
            self.send_error(404, f)

    def do_POST(self):
        length = self.headers.get('content-length')  # ヘッダーからボディーのデータ数を抽出
        nbytes = int(length)  # ボディーのデータ数を整数型に変換
        param_bytes = self.rfile.read(nbytes)  # ボディーのデータ(Bytes型)を抽出
        param_str = param_bytes.decode('utf-8')  # データをstr型に変換
        param_list = param_str.split('=')  # データをリスト型に変換
        param_dict = {param_list[0]: param_list[1]}  # データを辞書型に変換
        print(f'Body-param = {param_dict}です')

        # 関数ledcontrolの引数にデータを渡す
        # ledControl(param_dict["params"])

        ###URLを解析して処理を行いたい場合に記述（記録用）###
        # qs = urllib.parse.urlparse(url).query   #クエリ文字列をURLより抽出
        # res = urllib.parse.parse_qs(qs)         #クエリ文字列を辞書に変換？

        ###HTTPヘッダーにレスポンスを返す場合に必要（記録用）###
        # self.send_header("User-Agent","test1")
        self.send_response(200)  # POSTリクエストの受信成功を返答（ターミナルにも記載）
        self.send_header("Access-Control-Allow-Origin", '*')
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer((ip, port), MyHTTPReqHandler)
    print("---start web server by Python---")
    server.serve_forever()
