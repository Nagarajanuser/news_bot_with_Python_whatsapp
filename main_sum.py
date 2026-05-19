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


# GET NEWS
def get_latest_news():

    url = (
        f"https://newsdata.io/api/1/news?"
        f"apikey={NEWSDATA_API_KEY}"
        f"&q=israel iran war news"
        f"&category=world"
        f"&language=en"
        f"&size=5"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        print("NEWS API RESPONSE:", data)
        if data.get("status") == "success" and data.get("results"):
            return data["results"][:3]
        return []
    
    except Exception as e:
        print("News Fetch Error:", e)
        return []


# SUMMARIZE USING OLLAMA
def summarize_news(news_articles):

    if not news_articles:
        return "⚠️ No news available."

    news_text = ""

    for article in news_articles:

        title = article.get("title", "")
        source = article.get("source_id", "")
        date = article.get("pubDate", "")

        news_text += f"- {title} ({source} | {date})\n"

    prompt = f"""
    Summarize the following israel iran war news into short WhatsApp friendly bullet points.

    News:
    {news_text}
    """

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )
        result = response.json()
        summary = result["message"]["content"]
        return f"⚔️ *Israel-Iran War Summary*\n\n{summary}"

    except Exception as e:
        return f"❌ Ollama Error: {e}"


# SEND WHATSAPP MESSAGE
def send_whatsapp_message(message):

    try:
        client.messages.create(
            from_=FROM_WHATSAPP_NUMBER,
            body=message,
            to=TO_WHATSAPP_NUMBER
        )
        print("✅ WhatsApp message sent")

    except Exception as e:
        print("WhatsApp Error:", e)


# MAIN LOOP
while True:

    #print("Fetching latest news...")
    news_articles = get_latest_news()
    print("news_articles", news_articles)
    summarized_news = summarize_news(news_articles)
    print("summarized_news", summarized_news)
    send_whatsapp_message(summarized_news)
    print("⏳ Waiting 1 hour for next update...\n")
    time.sleep(3600)
