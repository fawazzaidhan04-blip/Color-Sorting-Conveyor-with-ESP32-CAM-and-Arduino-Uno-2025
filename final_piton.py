import cv2
import numpy as np
import requests
import time

# IP ESP32-CAM dan ESP32 biasa
cam_url = "http://192.168.158.28/capture"
esp32_ip = "http://192.168.158.250"

# Fungsi untuk mengambil gambar dari ESP32-CAM
def get_frame():
    try:
        img_resp = requests.get(cam_url, timeout=2)
        img_arr = np.frombuffer(img_resp.content, dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        return img
    except:
        print("Gagal mengambil gambar.")
        return None

# Fungsi untuk deteksi warna dominan
def detect_dominant_color(img, brightness_threshold=25):
    h, w, _ = img.shape
    crop = img[h//2-50:h//2+50, w//2-50:w//2+50]

    avg_color = np.average(np.average(crop, axis=0), axis=0)
    b, g, r = avg_color.astype(int)

    print(f"R: {r}, G: {g}, B: {b}")

    if r < brightness_threshold and g < brightness_threshold and b < brightness_threshold:
        return "Tidak Diketahui"

    if r > g and r > b:
        return "Merah"
    elif g > r and g > b:
        return "Hijau"
    elif b > r and b > g:
        return "Biru"
    else:
        return "Tidak Diketahui"

# Fungsi untuk kirim perintah ke ESP32 biasa
def kirim_perintah(warna):
    try:
        if warna == "Merah":
            response = requests.get(f"{esp32_ip}/servo1")
            print("Perintah dikirim ke servo1:", response.status_code)
        elif warna == "Hijau":
            response = requests.get(f"{esp32_ip}/servo2")
            print("Perintah dikirim ke servo2:", response.status_code)
        elif warna == "Biru":
            response = requests.get(f"{esp32_ip}/led")
            print("Perintah dikirim untuk menyalakan LED:", response.status_code)
    except:
        print("Gagal mengirim perintah ke ESP32.")

# Loop utama    
while True:
    frame = get_frame()
    if frame is not None:
        warna = detect_dominant_color(frame)
        print("Warna Dominan:", warna)

        # Kirim perintah hanya untuk Merah, Hijau, atau Biru
        if warna in ["Merah", "Hijau", "Biru"]:
            kirim_perintah(warna)
            time.sleep(2)  # delay untuk mencegah perintah terus-menerus

        # Tampilkan hasil
        cv2.putText(frame, warna, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imshow("Deteksi Warna", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()