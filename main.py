import requests
import os

def get_weather():
    key = os.environ.get("WEATHER_KEY")
    lat = 33.59   # 福冈
    lon = 130.40

    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={key}&units=metric&lang=zh_cn"
    data = requests.get(url).json()

    current = data["current"]
    today = data["daily"][0]

    temp_now = current["temp"]
    temp_max = today["temp"]["max"]
    temp_min = today["temp"]["min"]
    weather_desc = today["weather"][0]["description"]

    rain = today.get("rain", 0)

    # 简单判断建议
    if rain > 0:
        advice = "记得带伞 ☔"
    elif temp_max > 30:
        advice = "天气较热，注意防晒 🧴"
    else:
        advice = "适合外出 🌿"

    return f"""【福冈天气】
{weather_desc}
🌡 当前：{temp_now}℃
⬆️ 最高：{temp_max}℃
⬇️ 最低：{temp_min}℃
☔ 降雨：{'有' if rain else '无'}

建议：{advice}
"""

def send_wechat(msg):
    key = os.environ.get("SCKEY")
    url = f"https://sctapi.ftqq.com/{key}.send"

    requests.post(url, data={
        "title": "🌤 每日天气",
        "desp": msg
    })

if __name__ == "__main__":
    weather = get_weather()
    send_wechat(weather)
