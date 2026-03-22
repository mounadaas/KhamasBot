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

# 🔹 headers
headers = {"User-Agent": "Mozilla/5.0"}

# 🔹 أول تشغيل
first_run = True

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        res = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
        print("📤 Sent:", res.status_code)
    except Exception as e:
        print("❌ Error sending:", e)

def check_khamsat():
    global first_run

    url = "https://khamsat.com/community/requests"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        projects = soup.select("h3 > a[href^='/community/requests/']")
        times = soup.select("h3 span[dir='ltr']")

        now = datetime.now(timezone.utc)

        print("\n📌 Found:", len(projects))
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

            # 🔥 أول تشغيل
            if first_run:
                if diff <= timedelta(hours=2) and link not in sent_links:
                    print("🚀 FIRST RUN → Sending")
                    sent_links.add(link)
                    send_message(f"🔥 Khamsat\n{title}\n{link}")
                else:
                    print("⏭️ Skipped (first run)")

            # 🔥 بعد ذلك
            else:
                if diff <= timedelta(minutes=15) and link not in sent_links:
                    print("✅ NEW → Sending")
                    sent_links.add(link)
                    send_message(f"🔥 Khamsat NEW\n{title}\n{link}")
                else:
                    print("⏭️ Skipped")

        # 🔹 بعد أول دورة فقط
        if first_run:
            print("\n✅ First run completed → switching to 15 min mode")
            first_run = False

    except Exception as e:
        print("❌ Error:", e)

# 🔹 Start
send_message("✅ Khamsat bot started!")

while True:
    print("\n========================")
    print("🔄 Checking Khamsat...")
    check_khamsat()
    time.sleep(20)