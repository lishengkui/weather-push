import requests
import os

def get_weather():
    key = os.environ.get("WEATHER_KEY")
    city = "Fukuoka"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    data = requests.get(url).json()

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"福冈天气：{desc}，{temp}℃"

def send_wechat(msg):
    key = os.environ.get("SCKEY")
    url = f"https://sctapi.ftqq.com/{key}.send"

    requests.post(url, data={
        "title": "每日天气",
        "desp": msg
    })

if __name__ == "__main__":
    weather = get_weather()
    send_wechat(weather)
