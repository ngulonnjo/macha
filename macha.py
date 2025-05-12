import requests
import time
import json

SPIN_URL = "https://us-central1-andalasdroid.cloudfunctions.net/validateSpinReward"
TOKEN_URL = "https://securetoken.googleapis.com/v1/token?key=AIzaSyA392my-PuINFiHQtttX5Xwr7Fb5jCbEws"
REFRESH_TOKEN = "AMf-vBzIrBTVSlYwutL5jeoYYGRhFlbItPnbZYMlNO--HdaKgO4M7nQYyTqXHeb-QGHVmvtM2lqbVdvLtT8c5t0vFtBVI1vRJSJQA1L9UYhI2U_ydYY2Td90iBS-7Hemk7Fh6LLYMLaAOS_YtFxxLE54DlD_J-_idAXQM0gM05JmX2pnqklA_jwU-UMIWBT0fMKJ8Yeb-PXC4ZqeJRoh0FZCcXyZBs8rEw"

spin_data = {
    "data": {
        "userEmail": "muhammadsofyanayongulon@gmail.com",
        "requestedPoints": 2000
    }
}

common_headers = {
    "firebase-instance-id-token": "ewh_IsTHQrqC3ytX8ZWw8x:APA91bERNxtLEiQ2FVpol4kK4HxGNfGynoC4rYyRAPLwv4WpqcGkUGoT175lxXysRfGbKiwZ6uGhjcFRwr1ZETNS4TdLwkejPUN8-ZxIaxnW3iYYEawNTsc",
    "content-type": "application/json; charset=utf-8",
    "accept-encoding": "gzip",
    "user-agent": "okhttp/3.12.13"
}

def ambil_token():
    payload = {
        "grantType": "refresh_token",
        "refreshToken": REFRESH_TOKEN
    }
    headers = {
        "Content-Type": "application/json",
        "X-Android-Package": "com.andalasdev.mathchampion",
        "X-Android-Cert": "51DA0CB0979D29CF55FC80282CF5D17F0865AC02",
        "Accept-Language": "in-ID, en-US",
        "X-Client-Version": "Android/Fallback/X23002000/FirebaseCore-Android",
        "X-Firebase-GMPID": "1:784875757340:android:35f06779de2daea7fe64d9",
        "X-Firebase-Client": "H4sIAAAAAAAAAKtWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; M2102J20SG Build/RKQ1.200826.002)"
    }

    response = requests.post(TOKEN_URL, headers=headers, json=payload)
    if response.ok:
        id_token = response.json().get("id_token")
        print("Token baru berhasil diambil.")
        return id_token
    else:
        print("Gagal ambil token:", response.text)
        return None

def post_spin(token):
    headers = common_headers.copy()
    headers["authorization"] = f"Bearer {token}"
    response = requests.post(SPIN_URL, headers=headers, json=spin_data)

    if response.ok:
        data = response.json()
        if data.get("result", {}).get("success") is True:
            print("Spin sukses! Poin diperoleh:", data["result"].get("awardedPoints"))
            return True
        else:
            print("Spin gagal: respon tidak sukses.")
            return False
    else:
        print("Spin gagal dengan status:", response.status_code)
        return False

def countdown(sekon):
    for i in range(sekon, 0, -1):
        menit = i // 60
        detik = i % 60
        print(f"Tunggu {menit:02d}:{detik:02d} sampai spin berikutnya...", end='\r')
        time.sleep(1)
    print(" " * 60, end='\r')

def main():
    token = ambil_token()
    while True:
        print("\n[+] Menjalankan spin...")
        if not post_spin(token):
            print("[!] Gagal, ambil token baru...")
            token = ambil_token()
        countdown(600)  # 10 menit
