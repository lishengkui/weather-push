import requests
import os

def get_weather():
    key = os.environ.get("WEATHER_KEY")
    city = "Fukuoka"

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&units=metric&lang=zh_cn"
    res = requests.get(url)

    try:
        data = res.json()

        if "list" not in data:
            return f"API返回异常：{data}"

        # 当前（取第一个）
        current = data["list"][0]
        temp_now = current["main"]["temp"]
        desc = current["weather"][0]["description"]

        # 计算当天最高/最低
        temps = [item["main"]["temp"] for item in data["list"][:8]]  # 未来24小时
        temp_max = max(temps)
        temp_min = min(temps)

        # 判断是否有雨
        rain = any("rain" in item for item in data["list"][:8])

        if rain:
            advice = "记得带伞 ☔"
        elif temp_max > 30:
            advice = "天气较热，注意防晒 🧴"
        else:
            advice = "适合外出 🌿"

        return f"""【福冈天气】
{desc}
🌡 当前：{temp_now}℃
⬆️ 最高：{temp_max}℃
⬇️ 最低：{temp_min}℃
☔ 降雨：{'有' if rain else '无'}

建议：{advice}
"""

    except Exception as e:
        return f"天气获取失败：{e}"

def send_wechat(msg):
    key = os.environ.get("SCKEY")
    url = f"https://sctapi.ftqq.com/{key}.send"

    requests.post(url, data={
        "title": msg,
        "desp": ""
    })

if __name__ == "__main__":
    weather = get_weather()
    send_wechat(weather)
