#PythonGeeks - Import Modules
import random
import pygame
import sys
import pygame.mixer
import time
from pygame.locals import *
pygame.init()


start_time = pygame.time.get_ticks()
oyun_bitti = False
def main():
    global baslangic_zamani
    global oyun_bitti
    global score
    global start_time
    global deneme
    global Frame_Hiz_Saati, ekran
    pygame.init()
    Frame_Hiz_Saati = pygame.time.Clock()
    ekran = pygame.display.set_mode((pencere_gen, pencere_yuk))
 
    x_fare  = 0 
    y_fare = 0 
    pygame.display.set_caption('Memory Puzzle')
 
    Tahta = Randomized_Board()
    Kutular_acildi = GenerateData_RevealedBoxes(False)
 
    ilk_secim = None  
    ekran.fill(Arkaplan_Rengi)
    Oyunu_Baslat(Tahta)

    beyaz = (255, 255, 255)
    font = pygame.font.SysFont('Arial', 30)
    buton_menu = pygame.Rect(100, pencere_yuk - 40, 100, 30)
    buton_yeni= pygame.Rect(430,pencere_yuk - 40,190,30)
    renk_kolay = beyaz
    kirmizi = (255, 0, 0)

    while True: 
        
        fare_tiklamasi = False
          
        ekran.fill(Arkaplan_Rengi) 
        Tahtayi_ciz(Tahta, Kutular_acildi)
        gecen_zaman = time.time() - baslangic_zamani
        kalan_sure = oyun_suresi - gecen_zaman
        if kalan_sure <= 0:
            oyun_bitti = True
            kalan_sure = 0
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEMOTION:
                x_fare, y_fare = event.pos

            elif event.type == MOUSEBUTTONUP:
                x_fare, y_fare = event.pos
                fare_tiklamasi = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Fare tıklamasının koordinatları
                fare_x, fare_y = event.pos

                # Buton kontrolleri
                if buton_menu.collidepoint(fare_x, fare_y):
                    print('Menü seçildi!')
                    blup_ses.play()
                    import menu
                    menu.bas()
                if buton_yeni.collidepoint(fare_x,fare_y):
                    print('Yeni Oyun seçildi!')
                    blup_ses.play()
                    start_time = pygame.time.get_ticks()
                    score=0
                    deneme=0
                    main()

                if buton_geri.collidepoint(fare_x, fare_y):
                    print('Geri seçildi!')
                    blup_ses.play()
                    import klasik_menu
                    klasik_menu.bas()

        dakika = int(kalan_sure / 60)
        saniye = int(kalan_sure % 60)
        sure_metni = font.render("Kalan Süre: {:02d}:{:02d}".format(dakika, saniye), True, (255, 255, 255))
        
        sure_metni_pozisyon = sure_metni.get_rect()
        sure_metni_pozisyon.top = 10  # Metnin üst kenara olan mesafesi
        sure_metni_pozisyon.centerx = pencere_gen // 2  # Metnin yatay ortalanması
        ekran.blit(sure_metni, sure_metni_pozisyon)       

        uyari_metni = font.render("SÜRE BİTTİ!", True, kirmizi)
        uyari_metni_pozisyon = uyari_metni.get_rect()
        uyari_metni_pozisyon.center = (pencere_gen // 2, 65)
               
       
        pygame.draw.rect(ekran, renk_kolay, buton_menu,border_radius=10)
        metin_kolay = font.render('Menü', True, kirmizi)
        ekran.blit(metin_kolay, (buton_menu.x + 15, buton_menu.y -3))

        pygame.draw.rect(ekran, renk_kolay, buton_yeni,border_radius=10)
        metin_kolay = font.render('Yeniden Başla', True, kirmizi)
        ekran.blit(metin_kolay, (buton_yeni.x + 15, buton_yeni.y -3))
       
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        ekran.blit(score_text, (10, 10))
        deneme_text = font.render("Deneme: " + str(deneme), True, (255, 255, 255))
        ekran.blit(deneme_text, (500, 10))

        buton_geri = pygame.Rect(10, pencere_yuk - 40, 70, 30)
        metin_geri = font.render('←', True, kirmizi)
        pygame.draw.rect(ekran, beyaz, buton_geri,border_radius=30)
        ekran.blit(metin_geri, (buton_geri.x + 20, buton_geri.y-5 ))

        if oyun_bitti==False:
           

           kutu_x, kutu_y = kutu_pikseli(x_fare, y_fare)
           if kutu_x != None and kutu_y != None:
               if not Kutular_acildi[kutu_x][kutu_y]:
                   Draw_HighlightBox(kutu_x, kutu_y)
   
               if not Kutular_acildi[kutu_x][kutu_y] and fare_tiklamasi:
                   kutulari_acma_animas(Tahta, [(kutu_x, kutu_y)])
                   Kutular_acildi[kutu_x][kutu_y] = True 
   
                   if ilk_secim == None: 
                       ilk_secim = (kutu_x, kutu_y)
   
                   else:
                       ikon1_sekil, ikon1_renk = get_Shape_Color(Tahta, ilk_secim[0], ilk_secim[1])
                       ikon2_sekil, ikon2_renk = get_Shape_Color(Tahta, kutu_x, kutu_y)
   
                       if ikon1_sekil != ikon2_sekil or ikon1_renk != ikon2_renk:
                           yanlis_ses.play()
                           pygame.time.wait(500) 
                           
                           kutulari_kapatma_animas(Tahta, [(ilk_secim[0], ilk_secim[1]), (kutu_x, kutu_y)])
                           Kutular_acildi[ilk_secim[0]][ilk_secim[1]] = False
                           Kutular_acildi[kutu_x][kutu_y] = False
                           eksi_score(1)
                           
   
                       elif Won(Kutular_acildi): 
                           
                           Game_Won(Tahta)
                           pygame.time.wait(2000)
                       else:
                           dogri_ses.play()
                           arti_score(10) 
                           
                       arti_deneme(1)
                           
                       ilk_secim = None 
        elif oyun_bitti:
            ekran.blit(uyari_metni, uyari_metni_pozisyon) 
        pygame.display.update()
        Frame_Hiz_Saati.tick(oyun_hizi)
       
   





def GenerateData_RevealedBoxes(val):
    Boxes_revealed = []
    for i in range(oyun_tahta_gen):
        Boxes_revealed.append([val] * oyun_tahta_yuk)
    return Boxes_revealed     



#PythonGeeks- Creating a board
 
def Randomized_Board():
    ikon = []
    for renk in Tum_renkler:
        for sekil in Tum_sekiller:
            ikon.append( (sekil, renk) )
 
    random.shuffle(ikon) 
    kullanilan_ikon_say = int(oyun_tahta_gen * oyun_tahta_yuk / 2) 
    ikon = ikon[:kullanilan_ikon_say] * 2 
    random.shuffle(ikon)
 
    tahta = []
    for x in range(oyun_tahta_gen):
        sutun = []
        for y in range(oyun_tahta_yuk):
            sutun.append(ikon[0])
            del ikon[0] 
        tahta.append(sutun)
    return tahta



#PythonGeeks- Splitting a list into lists
 
def Split_Groups(grup_boyut, List):
    result = []
    for i in range(0, len(List), grup_boyut):
        result.append(List[i:i + grup_boyut])
    return result



#PythonGeeks- Create coordinate function
 
def sol_ust_konum(kutu_x, kutu_y):
    left = kutu_x * (kutu_buyuklugu + kutu_ara_bosluk) + x_orta
    top = kutu_y * (kutu_buyuklugu + kutu_ara_bosluk) + y_orta
    return (left, top)



#PythonGeeks- Converting to pixel coordinates to box coordinates
 
def kutu_pikseli(x, y):
    for kutu_x in range(oyun_tahta_gen):
        for kutu_y in range(oyun_tahta_yuk):
            left, top = sol_ust_konum(kutu_x, kutu_y)
            box_Rect = pygame.Rect(left, top, kutu_buyuklugu, kutu_buyuklugu)
            if box_Rect.collidepoint(x, y):
                return (kutu_x, kutu_y)
    return (None, None)



#PythonGeeks- Draw icon and synthetic sugar
 
def ikon_ciz(sekil, renk, kutu_x, kutu_y):
    ceyrek = int(kutu_buyuklugu * 0.25) 
    yarim    = int(kutu_buyuklugu * 0.5)  
 
    left, top = sol_ust_konum(kutu_x, kutu_y) 
 
    if sekil == CIRCLE:
        pygame.draw.circle(ekran, renk, (left + yarim, top + yarim), yarim - 5)
        pygame.draw.circle(ekran, Arkaplan_Rengi, (left + yarim, top + yarim), ceyrek - 5)
    elif sekil == SQUARE:
        pygame.draw.rect(ekran, renk, (left + ceyrek, top + ceyrek, kutu_buyuklugu - yarim, kutu_buyuklugu - yarim))
    elif sekil == DIAMOND:
        pygame.draw.polygon(ekran, renk, ((left + yarim, top), (left + kutu_buyuklugu - 1, top + yarim), (left + yarim, top + kutu_buyuklugu - 1), (left, top + yarim)))
    elif sekil == LINES:
        for i in range(0, kutu_buyuklugu, 4):
            pygame.draw.line(ekran, renk, (left, top + i), (left + i, top))
            pygame.draw.line(ekran, renk, (left + i, top + kutu_buyuklugu - 1), (left + kutu_buyuklugu - 1, top + i))
    elif sekil == OVAL:
        pygame.draw.ellipse(ekran, renk, (left, top + ceyrek, kutu_buyuklugu, yarim))
 
def get_Shape_Color(board, kutu_x, kutu_y):
    return board[kutu_x][kutu_y][0], board[kutu_x][kutu_y][1]




#PythonGeeks- Drawing box cover
 
def Box_Cover(tahta, koordinat, boyut):
    for box in koordinat:
        left, top = sol_ust_konum(box[0], box[1])
        pygame.draw.rect(ekran, Arkaplan_Rengi, (left, top, kutu_buyuklugu, kutu_buyuklugu))
        sekil, renk = get_Shape_Color(tahta, box[0], box[1])
        ikon_ciz(sekil, renk, box[0], box[1])
        if boyut > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(ekran, kutu_rengi, (left, top, boyut, kutu_buyuklugu))
    pygame.display.update()
    Frame_Hiz_Saati.tick(oyun_hizi)




#PythonGeeks- Revealing and covering animation
def kutulari_acma_animas(tahta, cikarilcak_kutular):
    for kaplama in range(kutu_buyuklugu, (-animas_hizi) - 1, -animas_hizi):
        Box_Cover(tahta, cikarilcak_kutular, kaplama)
 
def kutulari_kapatma_animas(tahta, kapanacak_kutu):
    for kaplama in range(0, kutu_buyuklugu + animas_hizi, animas_hizi):
        Box_Cover(tahta, kapanacak_kutu, kaplama)



#PythonGeeks- Drawing entire board and Highlight
 
def Tahtayi_ciz(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for x_box in range(oyun_tahta_gen):
        for y_box in range(oyun_tahta_yuk):
            left, top = sol_ust_konum(x_box, y_box)
            if not revealed[x_box][y_box]:                
                pygame.draw.rect(ekran, kutu_rengi, (left, top, kutu_buyuklugu, kutu_buyuklugu))

            else:
                shape, color = get_Shape_Color(board, x_box, y_box)
                ikon_ciz(shape, color, x_box, y_box)
 
def Draw_HighlightBox(kutu_x, kutu_y):
    left, top = sol_ust_konum(kutu_x, kutu_y)
    pygame.draw.rect(ekran, kutu_vurgu_rengi, (left - 5, top - 5, kutu_buyuklugu + 10, kutu_buyuklugu + 10), 4)




#PythonGeeks- Start the game animation
def Oyunu_Baslat(board):
    covered_Boxes = GenerateData_RevealedBoxes(False)
    boxes = []
    for x in range(oyun_tahta_gen):
        for y in range(oyun_tahta_yuk):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    box_Groups = Split_Groups(8, boxes)
    
    Tahtayi_ciz(board, covered_Boxes)
    for boxGroup in box_Groups:
        tiktak_ses.play()
        kutulari_acma_animas(board, boxGroup)
        kutulari_kapatma_animas(board, boxGroup)
        


#PythonGeeks- Creating function for game won
 
def Game_Won (board):
    coveredBoxes = GenerateData_RevealedBoxes(True)
    color_1 = bitirme_rengi
    color_2 = Arkaplan_Rengi
 
    for i in range(13):
        color_1, color_2 = color_2, color_1 
        ekran.fill(color_1)
        Tahtayi_ciz(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)
    
 
def Won(Boxes_revealed):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in Boxes_revealed:
        if False in i:
            return False 
    return True

def arti_score(points):
    global score
    score+=points
def eksi_score(points):
    global score
    score-=points
def arti_deneme(points):
    global deneme
    deneme+=points

tiktak_ses=pygame.mixer.Sound("tiktak.wav")  
yanlis_ses = pygame.mixer.Sound("ses.wav")
dogri_ses=pygame.mixer.Sound("final.wav")
blup_ses=pygame.mixer.Sound("blup.wav")
blup_ses.set_volume(0.1)
yanlis_ses.set_volume(0.1)
deneme=0
score=0
oyun_hizi = 30 
pencere_gen = 640 
pencere_yuk = 480
animas_hizi = 8 
kutu_buyuklugu = 40 
kutu_ara_bosluk = 10 
oyun_tahta_gen = 7 
oyun_tahta_yuk = 6 
oyun_suresi=300
baslangic_zamani=time.time()
assert (oyun_tahta_gen * oyun_tahta_yuk) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
x_orta = int((pencere_gen - (oyun_tahta_gen * (kutu_buyuklugu + kutu_ara_bosluk))) / 2)
y_orta = int((pencere_yuk - (oyun_tahta_yuk * (kutu_buyuklugu + kutu_ara_bosluk))) / 2)
 
#            R    G    B
Gray     = (100, 100, 100)
Navyblue = ( 60,  60, 100)
White    = (255, 255, 255)
Red      = (255,   0,   0)
Green    = (  0, 255,   0)
Blue     = (  0,   0, 255)
Yellow   = (255, 255,   0)
Orange   = (255, 128,   0)
Purple   = (255,   0, 255)
Cyan     = (0, 226, 226)
Acik_mavi= (173, 216, 230)
 
Arkaplan_Rengi = Gray
bitirme_rengi = Navyblue
kutu_rengi = Acik_mavi
kutu_vurgu_rengi = Yellow
 
CIRCLE = 'circle'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
 
Tum_renkler = (Red, Green, Cyan, Yellow, Orange, Purple, Blue)
Tum_sekiller = (CIRCLE, SQUARE, DIAMOND, LINES, OVAL)
assert len(Tum_renkler)* len(Tum_sekiller) * 2 >= oyun_tahta_gen * oyun_tahta_yuk, "Board is too big for the number of shapes/colors defined."
 
if __name__ == '__main__':
    main()



