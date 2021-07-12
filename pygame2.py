# import pygame & random
import pygame
import random

#import pygame.locals so keyboard access is simpler and more readable
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,

)
#----------------SETTING UP DISPLAY---------------------------------

#define constants for screen width and height
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000

#-------------CREATING PLAYER CLASS & ENEMY CLASS-----------------------------

#extend pygame.sprite.Sprite class,
#this will make surface an attribute of new Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('baush.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)

       #player bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#extend sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load('hornswoggle.png').convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1,3)

    #move sprite based on speed
    #remove sprite when it passes left edge of screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
#-----------------INITIALIZE PYGAME-----------------------------

#setup framerate clock
clock = pygame.time.Clock()

#ensures 30fps frame rate
clock.tick(30)

#initialize
pygame.init()

#create screen obj
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#create custom event for adding new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

#instantiate player
player = Player()

#creating enemy and sprite groups
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#--------------GAME LOOP + EVENT HANDLER--------------------------

#loop variable
running = True

#main loop
while running:
    #EVENT LOOP, checks if games running
    for event in pygame.event.get():
        #check keystroke
        if event.type == KEYDOWN:
            #if escape key, quit loop
            if event.key == K_ESCAPE:
                running = False

        #check if window close button was pressed
        elif event.type == QUIT:
            running = False

        #add new enemy?
        elif event.type == ADDENEMY:
            #create new enemy and add to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    #gets keys pressed and checks for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    #update enemy position
    enemies.update()

    #fill screen w black
    screen.fill((0, 0, 0))

    #draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #check for enemy collisions with player
    if pygame.sprite.spritecollideany(player, enemies):
        #remove player and end game
        player.kill()
        running = False

    #update display
    pygame.display.flip()
