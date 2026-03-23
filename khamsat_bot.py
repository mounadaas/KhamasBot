
# import os
# import time
# import requests
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv

# # قراءة .env
# load_dotenv()
# TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# CHAT_ID = os.getenv("CHAT_ID")

# # منع التكرار
# sent_links = set()

# def send_message(text):
#     url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
#     try:
#         requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
#     except Exception as e:
#         print("❌ Telegram Error:", e)

# def check_khamsat():
#     try:
#         response = requests.get(
#             "https://khamsat.com/community/requests",
#             headers={"User-Agent": "Mozilla/5.0"},
#             timeout=15
#         )
#         if response.status_code != 200:
#             print("❌ Failed to fetch page:", response.status_code)
#             return

#         soup = BeautifulSoup(response.text, "html.parser")
#         elements = soup.select("h3 a")  # العناصر التي تحتوي على العنوان والرابط

#         print("📊 Found projects:", len(elements))

#         for el in elements:
#             title = el.get_text(strip=True)
#             link = el.get("href")

#             # فلترة روابط المشاريع فقط
#             if not link or not link.startswith("/community/requests/"):
#                 continue

#             full_link = "https://khamsat.com" + link

#             if full_link not in sent_links:
#                 sent_links.add(full_link)
#                 print("✅ New project:", title)
#                 send_message(f"🚀 Khamsat Project\n{title}\n{full_link}")

#     except Exception as e:
#         print("❌ Error fetching projects:", e)

# # تشغيل البوت
# send_message("✅ Bot started successfully!")

# while True:
#     print("🔎 Checking for new projects...")
#     check_khamsat()
#     time.sleep(30)
import os
import time
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 🔹 قراءة .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔹 منع التكرار
sent_links = set()

# 🔹 إرسال رسالة على تيليجرام
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print("❌ Telegram Error:", e)

# 🔹 التحقق من المشاريع الجديدة
def check_khamsat():
    try:
        url = "https://khamsat.com/community/requests"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        project_elements = soup.select("h3 a")  # جميع روابط المشاريع

        print("📊 Found projects:", len(project_elements))

        # تحديد المشاريع الحديثة (مثلاً آخر 1 ساعة)
        recent_threshold = datetime.utcnow() - timedelta(hours=1)

        for el in project_elements:
            title = el.get_text(strip=True)
            link = el.get("href")

            # فلترة روابط المشاريع فقط
            if not link or not link.startswith("/community/requests/"):
                continue

            # الحصول على تاريخ النشر من span[title]
            time_el = el.find_next("span", title=True)
            if not time_el:
                continue

            publish_time_str = time_el["title"]  # مثل: "22/03/2026 22:48:22 GMT"
            try:
                # تحويل التاريخ إلى datetime
                publish_time = datetime.strptime(publish_time_str, "%d/%m/%Y %H:%M:%S GMT")
            except Exception as e:
                print("❌ Date parsing error:", e)
                continue

            # إذا المشروع قديم نتجاهله
            if publish_time < recent_threshold:
                continue

            full_link = "https://khamsat.com" + link
            if full_link not in sent_links:
                sent_links.add(full_link)
                print("✅ New project:", title)
                send_message(f"🚀 Khamsat Project\n{title}\n{full_link}")

    except Exception as e:
        print("❌ Scraping Error:", e)

# 🔹 تشغيل البوت
send_message("✅ Bot started successfully!")

while True:
    print("🔎 Checking for new projects...")
    check_khamsat()
    time.sleep(30)  # فحص كل 30 ثانية