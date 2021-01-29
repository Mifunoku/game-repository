import pygame, sys,os
from pygame.locals import *
import random
from pygame import mixer
import pygame_menu
import time

# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def volume(object,val):
    """Ustawianie dzwieku za pomoca przycisku sound_select"""
    if object[1]==1:
        mixer.music.set_volume(0.0)
    elif object[1]==0:
        mixer.music.set_volume(1.0)

def gameloop():
    """Pętla odpowiedzialna za grę"""
    #poczatkowe stale
    ball_name = selector1.get_value()[0]+'.png'
    ball1=pygame.image.load(ball_name)
    backx = 0
    backy = 0
    backvelo = 0
    jumpvelo = 0
    jumpvelo1 = 0
    lizakx = 1000
    lizakx2 = 2000
    lizakx3 = 2000
    lizaky = 353
    level=1
    skok = 0
    score=0
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
    zycie = pygame.image.load('life_on.png')
    obiekty = [lizak, ninja,lizak, ninja, krowa]
    obiekt1 = random.choice(obiekty)
    obiekt2 = random.choice(obiekty)
    obiekt3 = random.choice(obiekty)
    obiekt4 = random.choice(obiekty)
    font = pygame.font.SysFont('Comic Sans MS',20,True)
    # działa aż do kolizji

    while True:
        #ruch odbijania
        walk = [0, -3, -6, -9, -12, -15, -18, -21, -18, -15, -12, -9, -6, -3]
        # elementy
        ballx=15
        bally=378 + walk[walkpoint] + jumpy
        poziom = 2 ** level
        #level = int(((score/10)**0.5)/10)

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
                    if gravity.get_value()[1]==1:
                        jumpvelo = 3
                    else:
                        jumpvelo = 5*(level+1)
                    if crash_sound.get_value()[1] == 0:
                        if jumpy == 0:
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
        if jumpvelo != 0 and gravity.get_value()[1]!=1:
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

        score_text = font.render("Score: " + str(score),True,(0,0,0))
        #kolizja
        for i in range(0,4):
            if (bally+47 >= 353   and ((x_start[i] <=ballx+49<= x_end[i])or(x_start[i] <=ballx<= x_end[i]))) == True:
                if crash_sound.get_value()[1]==0:
                    explo_sound = mixer.Sound('explo2.wav')
                    explo_sound.play()
                backvelo = 0
                jumpvelo = 0
                walkpoint = 0
                dowalk = False
                zycie = pygame.image.load('life_off.png')
                stop_game = 1
                win.blit(score_text, [500, 200])
                k[str(player.get_value())]=score
                store_highscore_in_file(k, top_n=3)
                print(k)
                pygame.display.update()
                time.sleep(2)
                main()

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

def store_highscore_in_file(dictionary, fn = "./Highscores.txt", top_n=0):
    """Store the dict into a file, only store top_n highest values."""
    with open(fn,"w") as f:
        for idx,(name,pts) in enumerate(sorted(dictionary.items(), key= lambda x:-x[1])):
            f.write(f"{name}:{pts}\n")
            if top_n and idx == top_n-1:
                break

def load_highscore_from_file(fn = "./Highscores.txt"):
    """Retrieve dict from file"""
    hs = {}
    try:
        with open(fn,"r") as f:
            for line in f:
                name,_,points = line.partition(":")
                if name and points:
                    hs[name]=int(points)
    except FileNotFoundError:
        return {}
    return hs

def main():
    """Main function"""
    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    # utworzenie okna
    global win
    global selector1
    global crash_sound
    global menu
    global end_menu
    global sound_select
    global player
    global gravity
    global k
    global score
    score=0

    win = pygame.display.set_mode((1024, 500))
    pygame.display.set_caption("Ball-hop game")
    mixer.music.load('bg.wav')
    mixer.music.play(-1, 0)
    # -------------------------------------------------------------------------
    # Load highscore file
    # -------------------------------------------------------------------------
    k = load_highscore_from_file()
    store_highscore_in_file(k, top_n=5)
    a =[]
    for item,value in k.items():
        a.append(item)
        a.append(value)
    # -------------------------------------------------------------------------
    # Create menus
    # -------------------------------------------------------------------------
    #SETTINGS MENU
    settings_menu = pygame_menu.Menu(
        500, 1024,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=pygame_menu.themes.THEME_BLUE,
        title='Ustawienia',
    )
    sound_select = settings_menu.add_selector('Muzyka', [('Tak', 1), ('Nie', 0)], onchange=volume)
    crash_sound = settings_menu.add_selector('Dźwięki', [('Tak', 1), ('Nie', 0)])
    selector1 = settings_menu.add_selector('Wybierz piłkę :', [('koszykowa', 0), ('nożna', 1), ('siatkowa', 2)])
    gravity = settings_menu.add_selector('Grawitacja', [('Tak', 1), ('Nie', 0)])
    #RULES MENU
    zasady_menu = pygame_menu.Menu(
        500, 1024,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=pygame_menu.themes.THEME_BLUE,
        title='Jak grać?',
    )
    zasady_menu.add_label('''STEROWANIE: 
        Spacja=start/powrót gry, 
        strzałka w górę=skok, 
        p=pauza             
        ZASADY:                                        
            Skacz i unikaj przeszkód, masz jedno życie, zginiesz jeśli uderzysz w przeszkodę!
            Jeśli nie chcesz stracić swojego poprzedniego wyniku pamiętaj o zmianie nazwy!''',
                            max_char=45,
                            align=pygame_menu.locals.ALIGN_LEFT,
                            margin=(0, -1))
    #ABOUT AUTHOR MENU
    author_menu = pygame_menu.Menu(
        500, 1024,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=pygame_menu.themes.THEME_DARK,
        title='O autorze',
    )
    author_menu.add_label('''Autorem tego projektu jest skromny student matematyki stosowanej. Zafascynował się on programowaniem i gdyby nie lenistwo oraz brak organizacji byłby całkiem niezłym programistą. Dobrze, że się chociaż czasami stara...
    Cyprian Pełka''',
                            max_char=50,
                            align=pygame_menu.locals.ALIGN_LEFT,
                            margin=(0, -1))
    #RANK MENU
    rank_menu = pygame_menu.Menu(
        500, 1024,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=pygame_menu.themes.THEME_DARK,
        title='RANKING',
    )
    rank_menu.add_label(('Miejsce1.'+a[0]+':'+str(a[1])+'\nMiejsce2.'+a[2]+':'+str(a[3])+'\nMiejsce3.'+a[4]+':'+str(a[5])),
                            max_char=30,
                            align=pygame_menu.locals.ALIGN_CENTER,
                            margin=(0, -1))


    #MAIN MENU
    menu = pygame_menu.Menu(500, 1024, 'Witaj w świecie skaczącej piłki!',
                            onclose=pygame_menu.events.EXIT,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add_button('Start', gameloop)
    player = menu.add_text_input('Nazwa :', default='Skoczek')
    menu.add_button('Ranking', rank_menu)
    menu.add_button('Jak grać?', zasady_menu)
    menu.add_button('Ustawienia', settings_menu)
    menu.add_button('O autorze', author_menu)
    menu.add_button('Zakończ', pygame_menu.events.EXIT)

    menu.mainloop(win)

if __name__ == '__main__':
    main()