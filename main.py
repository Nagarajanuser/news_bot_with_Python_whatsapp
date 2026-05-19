import os
import requests
import time
from twilio.rest import Client
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

# Read values from .env
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP_NUMBER = os.getenv("FROM_WHATSAPP_NUMBER")
TO_WHATSAPP_NUMBER = os.getenv("TO_WHATSAPP_NUMBER")

# OLLAMA CONFIG
OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

# Initialize Twilio client
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)


def get_latest_news():
    url = (
        f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q=IPL Status&country=in&language=en"
    )
    response = requests.get(url)
    data = response.json()
    print('data',data)  # Debugging line to check the API response
    if data.get("status") == "success" and data.get("results"):
        messages = []
        for article in data["results"][:3]:
            title = article["title"]
            source = article.get("source_id", "Unknown")
            pub_date = article["pubDate"]
            link = article["link"]
            messages.append(f"🗞️ *{title}*\n📍{source} | 🕒 {pub_date}\n🔗 {link}")
        return "\n\n".join(messages)
    return "⚠️ No news found."

def send_whatsapp_message(message):
    client.messages.create(
        from_=FROM_WHATSAPP_NUMBER,
        body=message,
        to=TO_WHATSAPP_NUMBER
    )

while True:
    news = get_latest_news()
    send_whatsapp_message(news)
    time.sleep(3600)  # Every hour
