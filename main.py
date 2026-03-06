import feedparser
import schedule
import time
import requests
from googletrans import Translator
from telegram import Bot
import openai

# Telegram & OpenAI configs
TELEGRAM_TOKEN = "8783809477:AAG2NaaX5bhO4qj9SU5wHNcS9zgkRYfMgpg"
TELEGRAM_CHAT_ID = "5333799785"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

bot = Bot(token=TELEGRAM_TOKEN)
translator = Translator()
openai.api_key = OPENAI_API_KEY

# Read feeds
with open("news_sources.txt") as f:
    feeds = [line.strip() for line in f.readlines()]

posted_urls = set()

def fetch_news():
    global posted_urls
    for feed_url in feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # latest 5 entries per feed
            if entry.link not in posted_urls:
                # Fake news filter placeholder (implement your logic)
                if "fake" in entry.title.lower():
                    continue

                # AI summary
                summary = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": entry.title + " " + entry.summary}]
                )['choices'][0]['message']['content']

                # Translate to Somali
                summary_so = translator.translate(summary, src='en', dest='so').text

                # Send Telegram alert
                message = f"*{entry.title}*\n{summary_so}\n{entry.link}"
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')

                posted_urls.add(entry.link)

# Schedule 2-minute updates
schedule.every(2).minutes.do(fetch_news)

# Run forever
while True:
    schedule.run_pending()
    time.sleep(5)
