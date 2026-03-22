import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import time

# 🔹 env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔹 منع التكرار
sent_links = set()

headers = {"User-Agent": "Mozilla/5.0"}

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        res = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
        print("📤 Sent:", res.status_code)
    except Exception as e:
        print("❌ Error sending:", e)

def check_khamsat():
    url = "https://khamsat.com/community/requests"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        projects = soup.select("h3 > a[href^='/community/requests/']")

        print("📌 Found:", len(projects))

        for p in projects:
            title = p.text.strip()
            link = "https://khamsat.com" + p["href"]

            print("🔎 Checking:", title)

            if link not in sent_links:
                print("✅ Sending:", title)
                sent_links.add(link)
                send_message(f"🔥 Khamsat Project\n{title}\n{link}")
            else:
                print("⏭️ Already sent")

    except Exception as e:
        print("❌ Error:", e)

# 🔹 Start message
send_message("✅ Khamsat bot started!")

while True:
    print("\n🔄 Checking Khamsat...")
    check_khamsat()
    time.sleep(20)