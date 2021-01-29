import pygame, sys,os
from pygame.locals import *
import random
from pygame import mixer

mixer.pre_init(44100,-16,1,512)
pygame.init()
# utworzenie okna
win = pygame.display.set_mode((1024, 500))
pygame.display.set_caption("T-rex game")

def gameloop():
   """Pętla odpowiedzilna za grę"""
   #poczatkowe stale
   backx = 0
   backy = 0
   backvelo = 0
   jumpvelo = 0
   jumpvelo1 = 0
   lizakx = 1000
   lizakx2 = 2000
   lizakx3 = 2000
   lizaky = 353
   level=0
   score=3000
   skok = 0
   gravity=1
   a,b,c,d,e=random.randint(300, 500),random.randint(300, 500),random.randint(300, 500),random.randint(300, 500),random.randint(300, 500)
   jumpy = 0
   stop_game=1
   clock= pygame.time.Clock()
   walkpoint = 0
   dowalk = True
   lizak = pygame.image.load('lizak.png')
   ninja = pygame.image.load('ninja.png')
   krowa = pygame.image.load('krowa.png')
   background = pygame.image.load('tlo2.png')
   zycie = pygame.image.load('life on.png')
   obiekty = [lizak, ninja,lizak, ninja, krowa]
   obiekt1 = obiekty[random.choice([0, 1, 2])]
   obiekt2 = obiekty[random.choice([0, 1, 2])]
   obiekt3 = obiekty[random.choice([0, 1, 2])]
   obiekt4 = obiekty[random.choice([0, 1, 2])]
   font = pygame.font.SysFont('Comic Sans MS',20,True)
   # działa aż do przerwania
   mixer.music.load('bg.wav')
   mixer.music.play(-1, 0)

   while True:
      #ruch odbijania
      walk = [0, -3, -6, -9, -12, -15, -18, -21, -18, -15, -12, -9, -6, -3]
      # elementy
      ball1 = pygame.image.load('basket2.png')
      ballx=15
      bally=378 + walk[walkpoint] + jumpy
      poziom = 2 ** level
      level = int(((score/10)**0.5)/10)

      for event in pygame.event.get():
         if event.type == QUIT:
            sys.exit(0)
         if event.type == KEYDOWN:
            if event.key  == 32:
               """Click Space to start/resume game"""
               backvelo = 5*poziom #predkosc przesuwania ekranu
               jumpvelo=jumpvelo1
               stop_game=0
               walkpoint=0
            if event.key == 273 and stop_game==0:
               """Click up arrow key to Jump"""
               if gravity == 0:
                  jumpvelo = poziom
               else:
                  jumpvelo = 5*(level+1)
               jump_sound = mixer.Sound('jump2.wav')
               jump_sound.play()
            if event.key == K_p:
               """Click p to stop game"""
               backvelo = 0
               jumpvelo1=jumpvelo
               jumpvelo = 0
               stop_game=1

      if stop_game==0:
         score+=1+level
      if backvelo != 0:
         backvelo = 5 * poziom
      if jumpvelo != 0:
         jumpvelo = 5*(level+1)

      backx -= backvelo #poruszanie sie obrazu

      if skok == 0:
         jumpy -= 1.5*jumpvelo
      if skok == 1:
         jumpy += jumpvelo
      if jumpy <= -180:
         skok = 1
         walkpoint = 0
      if jumpy == 0:
         jumpvelo = 0
         if dowalk == True:
            walkpoint += 1
         skok = 0
      if walkpoint == 14:
         walkpoint = 0

      if backx<=-1000:
         backx=0

   #przesuwanie sie obiektow razem z tlem
      lizakx -= backvelo
      lizakx2 -= backvelo
      lizakx3 -= backvelo

      if lizakx == -(900+100*poziom):
         lizakx = random.randrange(1000, 1200, 5*poziom)
         a = random.randint(350+50*poziom,500+100*poziom)
         b = random.randint(250+50*poziom,500+100*poziom)
         obiekt1 = obiekty[random.choice([0,1,2])]
         obiekt2 = obiekty[random.choice([0,1,2,3,4])]

      if lizakx == 100:
         lizakx2 = lizakx+a+b
         lizakx3 = lizakx2
         obiekt3 = obiekty[random.choice([0,1,2,3,4])]
         obiekt4 = obiekty[random.choice([0,1,2,3,4])]
         d = random.randint(300+50*poziom,400+100*poziom)

      obiekt=[obiekt1,obiekt2,obiekt3,obiekt4]
      x_start=[lizakx,lizakx+a,lizakx3,lizakx3 + d]
      x_end=[lizakx+obiekt1.get_width(), lizakx+a+obiekt2.get_width(), lizakx3+obiekt3.get_width(), lizakx3 + d+obiekt4.get_width()]

      #kolizja
      for i in range(0,4):
         if (bally+47 >= 353   and ((x_start[i] <=ballx+49<= x_end[i])or(x_start[i] <=ballx<= x_end[i]))) == True:
            explo_sound = mixer.Sound('explo2.wav')
            explo_sound.play()
            backvelo = 0
            jumpvelo = 0
            walkpoint = 0
            dowalk = False
            zycie = pygame.image.load('life off.png')
            stop_game = 1

      score_text = font.render("Score: " + str(score),True,(0,0,0))

      win.blit(background, [backx, backy])#1000,424
      win.blit(background, [backx+1000, backy])
      win.blit(zycie, [990,20])
      win.blit(score_text, [800, 20])
      win.blit(ball1, [ballx,bally] ) #424-47
      win.blit(obiekt1, [lizakx, lizaky])
      win.blit(obiekt2, [lizakx+a, lizaky])
      win.blit(obiekt3, [lizakx3, lizaky])
      win.blit(obiekt4, [lizakx3 + d, lizaky])


      pygame.display.update()
      clock.tick(30)