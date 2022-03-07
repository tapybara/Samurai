import requests

def lineNotify(param):
    url = "https://notify-api.line.me/api/notify" 
    token = "Y385ARnvBMnIT8xVbHkab0h7G5y7Lgk9jhro0xaCohV"
    headers = {"Authorization" : "Bearer "+ token} 
    message =  f"LEDが{param}されました" 
    payload = {"message" :  message} 
    r = requests.post(url, headers = headers, params=payload)