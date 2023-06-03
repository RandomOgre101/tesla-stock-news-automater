import requests
import datetime as dt
from datetime import timedelta
from twilio.rest import Client


twilio_sid = "TWILIO_SID"
auth_token = "AUTH_TOKEN"
twilio_num = "TWILIO_NUMBER"
client = Client(twilio_sid, auth_token)


today = dt.date.today()
yesterday = today- timedelta(days = 1)
day_before = today - timedelta(days = 2)


stock_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=TSLA&apikey=API_KEY"
r_stock = requests.get(url=stock_url)
r_stock.raise_for_status
stock_data = r_stock.json()

yday_close = float(stock_data["Time Series (Daily)"][str(yesterday)]["4. close"])
day_before_close = float(stock_data["Time Series (Daily)"][str(day_before)]["4. close"])

diff_temp = yday_close - day_before_close
avg_temp = (yday_close + day_before_close)/2
change = round((diff_temp/avg_temp)*100)


news_url = 'https://newsapi.org/v2/everything?q="Tesla%20Inc"&apiKey=API_KEY'
r_news = requests.get(url=news_url)
r_news.raise_for_status
news_data = r_news.json()
headline = news_data["articles"][0]["title"]
brief = news_data["articles"][0]["content"].split(" [")[0]
link = news_data["articles"][0]["url"]


if change > 0:
    message = client.messages.create(
    body=f"TSLA: 🔺{change}%\nHeadline: {headline}\nBrief: {brief}\{link}",
    from_="TWILIO_NUM",
    to="TO_NUM"
    )

elif change < 0:
    message = client.messages.create(
    body=f"TSLA: 🔻{change}%\nHeadline: {headline}\nBrief: {brief}\{link}",
    from_="TWILIO_NUM",
    to="TO_NUM"
    )

