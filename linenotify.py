import os
import requests

def lineNotify(param, text):
    url = "https://notify-api.line.me/api/notify" 
    token = os.environ["token_lineNotify"]
    headers = {"Authorization" : "Bearer "+ token} 
    message =  text 
    payload = {"message" :  message} 
    r = requests.post(url, headers = headers, params=payload)