import sys
import pygame 
import datetime
import pygame.mixer

from pygame.locals import *
pygame.init()

# Ekran boyutu
ekran_genislik = 640
ekran_yukseklik = 480

# Renkler
gray =(100, 100, 100)
beyaz = (255, 255, 255)
kirmizi = (255, 0, 0)

# Font ayarları
font = pygame.font.SysFont('Arial', 30)

# Ekran
ekran = pygame.display.set_mode((ekran_genislik, ekran_yukseklik))
pygame.display.set_caption('Memory Puzzle')

# Buton renkleri
renk_kolay = gray
renk_orta = gray
renk_zor = gray
def bas():

    # Oyun döngüsü
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Fare tıklamasının koordinatları
                fare_x, fare_y = event.pos

                # Buton kontrolleri
                if buton_kolay.collidepoint(fare_x, fare_y):
                    print('klasik seçildi!')
                    blup_ses.play()
                    import klasik_menu
                    klasik_menu.bas()
                    # Burada kolay seçeneğinde yapılacak işlemler olabilir.

                if buton_orta.collidepoint(fare_x, fare_y):
                    print('Puanlı seçildi!')
                    blup_ses.play()
                    import puanli_menu
                    puanli_menu.bas()
                    
                    # Burada orta seçeneğinde yapılacak işlemler olabilir.

                if buton_zor.collidepoint(fare_x, fare_y):
                    print('Süreli seçildi!')
                    blup_ses.play()
                    import sureli_menu
                    sureli_menu.bas()
                    # Burada zor seçeneğinde yapılacak işlemler olabilir.

        # Arayüzü temizle
        ekran.fill(gray)
      
        # Butonları çiz
        image_path = '1.2.png'
        image = pygame.image.load(image_path)
        ekran.blit(image, (0,0))


        buton_kolay = pygame.Rect(75, 90, 130, 52)
        buton_orta = pygame.Rect(75, 215, 130, 52)
        buton_zor = pygame.Rect(75, 340, 130, 52)

        # Butonlara metin yazısı ekle
        metin_kolay = font.render('Klasik', True, kirmizi)
        metin_orta = font.render('Puanlı', True, kirmizi)
        metin_zor = font.render('Süreli', True, kirmizi)

        pygame.draw.rect(ekran, renk_kolay, buton_kolay)
        pygame.draw.rect(ekran, renk_orta, buton_orta)
        pygame.draw.rect(ekran, renk_zor, buton_zor)
        
        

        ekran.blit(metin_kolay, (buton_kolay.x + 10, buton_kolay.y + 10))
        ekran.blit(metin_orta, (buton_orta.x + 10, buton_orta.y + 10))
        ekran.blit(metin_zor, (buton_zor.x + 10, buton_zor.y + 10))

        # Ekranı güncelle
        pygame.display.update()
blup_ses=pygame.mixer.Sound("blup.wav")  
blup_ses.set_volume(0.1)     



if __name__ == '__main__':
    bas()
