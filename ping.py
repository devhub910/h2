import socket
import time
import struct

# دالة فحص الاتصال بالخادم
def check_minecraft_server(ip, port):
    try:
        # إنشاء سوكيت للاتصال بالخادم
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # تحديد مهلة الاتصال بـ 5 ثوانٍ

        # محاولة الاتصال بالخادم
        start_time = time.time()
        result = sock.connect_ex((ip, port))
        
        response_time = time.time() - start_time  # وقت الاستجابة
        
        if result == 0:
            print(f"[+] The Minecraft server at {ip}:{port} is reachable!")
            print(f"Server response time: {response_time:.2f} sec")
            print("[+] DDoS attack is possible on this server.")
            
            # بدء فحص البنق بشكل مستمر كل 2 ثانية
            while True:
                print(f"Checking Ping...")
                ping = check_ping(ip, port)
                print(f"Current Ping: {ping} ms")
                time.sleep(2)  # الانتظار لمدة 2 ثانية قبل الفحص التالي
                
        else:
            print(f"[X] Failed to reach the Minecraft server at {ip}:{port}")
        
        # إغلاق الاتصال بعد الفحص
        sock.close()

    except Exception as e:
        print(f"[!] Error occurred while checking the server: {e}")

# دالة فحص البنق
def check_ping(ip, port):
    try:
        # إنشاء سوكيت للاتصال بالخادم
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        start_time = time.time()  # بدء قياس وقت الاستجابة
        sock.connect((ip, port))
        ping_time = time.time() - start_time  # حساب الوقت المستغرق
        
        sock.close()  # إغلاق الاتصال بعد القياس
        return round(ping_time * 1000)  # تحويل إلى ميلي ثانية

    except Exception as e:
        print(f"[!] Error occurred while checking ping: {e}")
        return -1  # في حال فشل القياس

# بيانات الخادم
ip = "FronzFR.aternos.me"
port = 49208

# تنفيذ الفحص
check_minecraft_server(ip, port)