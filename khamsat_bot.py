import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timezone, timedelta

# 🔹 env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔹 منع التكرار
sent_links = set()

headers = {"User-Agent": "Mozilla/5.0"}

# 🔹 نأخذ آخر 15 دقيقة
TIME_WINDOW = timedelta(minutes=15)

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
        times = soup.select("h3 span[dir='ltr']")

        now = datetime.now(timezone.utc)

        print("📌 Found:", len(projects))
        print("🕒 Current time:", now)

        for p, t in zip(projects, times):
            title = p.text.strip()
            link = "https://khamsat.com" + p["href"]

            try:
                project_time = datetime.strptime(
                    t["title"], "%d/%m/%Y %H:%M:%S GMT"
                ).replace(tzinfo=timezone.utc)
            except Exception as e:
                print("⚠️ Time parse error:", e)
                continue

            diff = now - project_time

            print("\n🔎 Project:", title)
            print("🕒 Published:", project_time)
            print("⏱️ Diff:", diff)

            # 🔥 الشرط الصحيح
            if diff <= TIME_WINDOW and link not in sent_links:
                print("✅ NEW → Sending")
                sent_links.add(link)
                send_message(f"🔥 Khamsat NEW\n{title}\n{link}")
            else:
                print("⏭️ OLD or already sent")

    except Exception as e:
        print("❌ Error:", e)

# 🔹 Start
send_message("✅ Khamsat bot started!")

while True:
    print("\n========================")
    print("🔄 Checking Khamsat...")
    check_khamsat()
    time.sleep(20)