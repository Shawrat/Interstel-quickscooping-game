import random
import pygame
import math
from pygame import mixer
#initializing pygame
pygame.init()

screen = pygame.display.set_mode((800,600))

background = pygame.image.load('interstele.png')

endgame_placard = pygame.image.load('peakgameoverkewk.jpg')

#background based music by based people
mixer.music.load('quickscooperbasedaudiofileconfidential.mp3')
mixer.music.play(-1)

#title and stuff
pygame.display.set_caption("Interstellar Knockoff")
icon = pygame.image.load('heptapods.png')
pygame.display.set_icon(icon)

#player
playerimg = pygame.image.load('001-spaceship.png')
playerX = 370
playerY = 480
playerXposchange = 0

#enemy
enemyimg = []
enemyX = []
enemyY = []
enemyXposchange = []
enemyYposchange = []
no_of_enemies = 7

for i in range (0,no_of_enemies):
    enemyimg.append(pygame.image.load('laughing.png'))
    enemyX.append(random.randint(0,735))  
    enemyY.append(random.randint(50,150)) 
    enemyXposchange.append(4)
    enemyYposchange.append(40)

#bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletXposchange = 0
bulletYposchange = 10
bulletstate = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf',20)
textX = 10
textY = 10

def display_score(x,y):
    scooper = font.render("Quickscoop count :" + str(score),True, (255,255,255))
    screen.blit(scooper, (x,y))

def game_over_placard():
    screen.blit(endgame_placard, (20, 10))

def player(x,y):
    screen.blit(playerimg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyimg[i], (x, y))

def firebullet (x,y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletimg,(x+16, y+10))

def collision (enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX-bulletX),2))+(math.pow((enemyY-bulletY),2)))
    if distance < 27 :
        return True
    else:
        return False

#main game loop
running = True 
while running:
    #rgb
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #controlling it using keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXposchange = -7
            if event.key == pygame.K_RIGHT:
                playerXposchange = +7
            if event.key == pygame.K_SPACE:
                if bulletstate == "ready":
                    bulletX = playerX
                    firebullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXposchange = 0

    #boundary correction
    playerX = playerX + playerXposchange
    if playerX <= 0 :
        playerX = 0
    elif playerX >=736 :
        playerX = 736

    for i in range (0,no_of_enemies):
        #game over
        if enemyY[i] > 440 :
            for j in range (no_of_enemies):
                enemyY[j] = 2000
            game_over_placard()
            break

        enemyX[i] = enemyX[i] + enemyXposchange[i]
        if enemyX[i] <= 0 :
            enemyXposchange[i] = 5
            enemyY[i] += enemyYposchange[i]
        elif enemyX[i] >=736 :
            enemyXposchange[i] = -5
            enemyY[i] += enemyYposchange[i]

        #collision
        collide = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collide :
            collision_sound = mixer.Sound('focus_change_fastscroll.wav')
            collision_sound.play()
            bulletY=480
            bulletstate = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bulletstate = "ready"
    if bulletstate is "fire":
        firebullet(bulletX, bulletY)
        bulletY -= bulletYposchange

    

    player(playerX, playerY)
    #enemy(enemyX, enemyY)
    display_score(textX, textY)
    pygame.display.update()        