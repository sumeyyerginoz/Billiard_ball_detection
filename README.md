# Billiard_ball_detection
Bu Python programı, bir bilardo oyunundaki topu tespit etmek, rengini belirlemek ve hareketini izlemek için görüntü işleme tekniklerini kullanır. Program, OpenCV kütüphanesiyle yazılmıştır ve bilardo masasındaki farklı renkteki topları (kırmızı, sarı, beyaz) tanımlayabilir.

## Gereksinimler

Python 3.x
OpenCV (cv2)
NumPy

## Kurulum

OpenCV ve NumPy kütüphanelerini yüklemek için terminal veya komut istemcisinde aşağıdaki komutları çalıştırın:
pip install opencv-python
pip install numpy

## Kullanım

Kodu bilgisayarınıza kaydedin.
Bir bilardo videosunu veya kamera görüntüsünü kullanarak programı çalıştırın:
Copy code
python billiard_ball_detection.py
Program, bilardo masasındaki topları tespit edecek ve hareket izini çizecektir.
Çıkış yapmak için ekrandaki herhangi bir pencereye tıklayıp "q" tuşuna basın.

## Renk Tespiti
![gyuw4](https://github.com/sumeyyerginoz/Billiard_ball_detection/assets/112480236/f75c7162-2baf-4684-8a3a-2f65a6d7a807) <br>
Renk tespitinde kırmızı renk için 2 renk aralığı belirtmemizin sebebi HSV renk uzayında kırmızı rengin iki renk alanında bulunmasıdır.
Beyaz top için renk aralığı: HSV (0-179, 0-30, 200-255)
Kırmızı top için renk aralığı: HSV (0-5, 100-255, 150-255) ve (160-179, 100-255, 100-255)
Sarı top için renk aralığı: HSV (22-33, 100-255, 100-255)

##Ekran Çıktısı
Start 
![Ekran Resmi 2024-04-24 13 10 46](https://github.com/sumeyyerginoz/Billiard_ball_detection/assets/112480236/b06476f4-e535-48f0-a920-960d29d702aa)
![Ekran Resmi 2024-04-24 13 10 57](https://github.com/sumeyyerginoz/Billiard_ball_detection/assets/112480236/ce80ac00-3074-496d-bd56-904ff376e8bc)
Finish
![Ekran Resmi 2024-04-24 13 10 51](https://github.com/sumeyyerginoz/Billiard_ball_detection/assets/112480236/3b93f17b-7dee-4702-8248-05deb47ab6d7)
