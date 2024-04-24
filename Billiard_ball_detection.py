#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:40:38 2024

@author: sumeyye
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 20:07:39 2024

@author: sumeyye
"""

import cv2
import numpy as np
import math
 
prev_center = None
 # Kırmızı, sarı ve beyaz renklerin HSV aralıklarını tanımlama 
 #renkleri her yerde kullandığım için global değişken olarak tanımladım
lower_red1 = np.array([0, 100, 150])
upper_red1 = np.array([5, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])
lower_yellow = np.array([22, 100, 100])
upper_yellow = np.array([33, 255, 255])
lower_white = np.array([0, 0, 200])
upper_white = np.array([179, 30, 255])
# top tespiti fonksiyonu kırmızı,sarı ve bayz için tek tek renk aralıkları belirlendi
def detect_billiard_balls(frame):
    global prev_center

    # Kareyi HSV renk uzayına dönüştürün
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Renk maskeleri oluşturun
    red_mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    #kırmızının renk aralığı 2 alana yayılmış durumda 
    
    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    white_mask = cv2.inRange(hsv_frame, lower_white, upper_white)

    # Maskeleri birleştirme 
    combined_mask = cv2.bitwise_or(red_mask1, red_mask2)
    combined_mask = cv2.bitwise_or(combined_mask, yellow_mask)
    combined_mask = cv2.bitwise_or(combined_mask, white_mask)
    cv2.imshow("ikili maske gorunumu",combined_mask) 

    # Maskeleri kullanarak nesnelerin konturlarını bulma
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Belirli bir boyut aralığındaki nesneleri tespit etmek için filtreleme
    min_area = 77  # En küçük kabul edilebilir kontur alanı
    max_area = 777  # En büyük kabul edilebilir kontur alanı

    for contour in contours:
        area = cv2.contourArea(contour)

        if min_area < area < max_area:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)  # Yeşil renkte dikdörtgen çizin

            # Merkez pikseli alarak renk etiketini belirleyin
            x, y, w, h = cv2.boundingRect(contour)
            centroid_x = x + w // 2
            centroid_y = y + h // 2
            hsv_pixel = hsv_frame[centroid_y, centroid_x]
            color_label = determine_color(hsv_pixel)


            # sarı,kırmızı ve beyazın dışındaysa işlem yapmayacak
            if color_label != "RENK BULUNAMADI":
                cv2.putText(frame, color_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

  
         # Merkez koordinatlarını güncelleme ve kırmızı topun hareket çizgisi çizme
                center = (centroid_x, centroid_y)
                if prev_center is not None:
                    cv2.line(frame, prev_center, center, (255, 0, 215), 2)  # MAVİ renkte çizgi çizin opsiyonel
                    # Hızı hesaplama işlemi
                    speed = calculate_speed(prev_center, center)
                    cv2.putText(frame, f"pixels/frame hizi: {speed:.2f} ", center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0),2)
                prev_center = center

    return frame

# Renk belirleme fonksiyonu
def determine_color(hsv_pixel):
    hue = hsv_pixel[0]
    saturation = hsv_pixel[1]
    value = hsv_pixel[2]

    if (0 <= hue <= 5 or 165 <= hue <= 179) and (255> saturation > 100) and value > 100:
        return "KIRMIZI"
    elif 22 <= hue <= 33 and saturation > 100 and value > 100:
        return "SARI"
    elif saturation < 30 and value > 200:
        return "BEYAZ"
    else:
        return "RENK BULUNAMADI"

# Hız hesaplama fonksiyonu
def calculate_speed(prev_pos, current_pos, frame_rate=30):
    

    # İki nokta arasındaki mesafeyi hesapla
    distance = np.linalg.norm(np.array(current_pos) - np.array(prev_pos))
    # Hızı kareler arası zamanla çarp
    speed = distance * frame_rate
    return speed

def detect_color_objects(frame, lower_bound, upper_bound, color_name):
    
    # Kareyi HSV renk uzayına dönüştür
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Renk maskesi oluştur
    color_mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

    # Maskenin konturlarını bul
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Belirli bir boyut aralığındaki nesneleri tespit etmek için filtrele
    min_area = 100  # En küçük kabul edilebilir kontur alanı
    max_area = 1000  # En büyük kabul edilebilir kontur alanı

    for contour in contours:
        area = cv2.contourArea(contour)

        if min_area < area < max_area:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)  # Yeşil renkte dikdörtgen çiz

            # Merkez pikseli alarak renk etiketini belirle
            x, y, w, h = cv2.boundingRect(contour)
            centroid_x = x + w // 2
            centroid_y = y + h // 2

            # Merkezi işaretle
            cv2.circle(frame, (centroid_x, centroid_y), 5, (255, 0, 0), -1)
            cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return frame


# Video dosyasını açma
camera = cv2.VideoCapture("/Users/sumeyye/Desktop/imageProcesswork/vid_1.avi") 

width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(width, height) #tespit edilen videonun boyutu öğrenilir ve masa dışındaki alanlar blurlanır


while True:
    ret, frame = camera.read()
    if not ret:
        break

    # Görüntüyü HSV renk uzayına dönüştürün
    #HSV renk uzayını kullandığımız için kırmızı için 2 renk aralığı mevcut
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Beyaz top için renk aralığı global değişkendeki değerleri kullanarak white_frame işlemini gerçekleştirecek
    white_frame = detect_color_objects(frame.copy(), lower_white, upper_white, "WHITE")

    # Kırmızı top için renk aralığı global değişkendeki değerleri kullanarak red_frame işlemini gerçekleştirecek
    red_frame = detect_color_objects(frame.copy(), lower_red2, upper_red2, "RED")

    # Sarı top için renk aralığı global değişkendeki değerleri kullanarak yellow_frame işlemini gerçekleştirecek
    yellow_frame = detect_color_objects(frame.copy(), lower_yellow, upper_yellow, "YELLOW")

    red_mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
    white_mask = cv2.inRange(hsv_frame, lower_white, upper_white)
    
    # Renkleri ayrı ayrı ekranlarda göster
    cv2.imshow("Beyaz Top Tespiti", white_frame)
    cv2.imshow("Kirmizi Top Tespiti", red_frame)
    cv2.imshow("Sari Top Tespiti", yellow_frame)

    cv2.imshow("Orijinal", frame)

    # Yeşil renk aralığını tanımlayın (bilardo masası için genellikle yeşil tonları)
    lower_green = np.array([30, 40, 30])
    upper_green = np.array([100, 255, 255])

    # Yeşil renk aralığını kullanarak masayı tespit etmek için maske oluşturun
    mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    # Maskeyi kullanarak masanın konturlarını bulun
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # En büyük konturu bulun (muhtemelen masanın konturu)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        # Masanın çevresini çiz
        cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 2)


    cv2.imshow("Bilardo Masasi Tespiti", frame)
    detected_frame = detect_billiard_balls(frame)

    cv2.imshow("Tespit Edilen Toplar", detected_frame)
    

    # 'q' tuşuna basıldığında çıkış yap
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()

# Tüm pencereleri kapat
cv2.destroyAllWindows()