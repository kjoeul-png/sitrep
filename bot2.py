import anthropic
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Bot
import schedule, time, threading, asyncio, os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ANTHROPIC_KEY = os.environ["ANTHROPIC_KEY"]
MY_CHAT_ID = None
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

async def handle(update, ctx):
    global MY_CHAT_ID
    MY_CHAT_ID = update.message.chat_id
    msg = update.message.text
    r = client.messages.create(model="claude-haiku-4-5-20251001",max_tokens=500,messages=[{"role":"user","content":msg}])
    await update.message.reply_text(r.content[0].text)

def send_briefing():
    if MY_CHAT_ID is None:
        return
    r = client.messages.create(model="claude-haiku-4-5-20251001",max_tokens=800,messages=[{"role":"user","content":"오늘 한국 국방 안보 주요 뉴스 3가지 브리핑해줘"}])
    bot = Bot(token=TELEGRAM_TOKEN)
    asyncio.run(bot.send_message(chat_id=MY_CHAT_ID, text=r.content[0].text))

def scheduler():
    schedule.every().day.at("07:00").do(send_briefing)
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=scheduler, daemon=True).start()
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
print("Claude 봇 켜짐!")
app.run_polling()
