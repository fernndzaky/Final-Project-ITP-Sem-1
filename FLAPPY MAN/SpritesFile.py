# Sprite classes for platform game
import pygame as pg
from SettingsFile import *


#acceleration
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/Man-flying.png")

        self.image = pg.transform.scale(self.image,(55 ,40))
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-10,-5)
        self.rect.center = (WIDTH /2, HEIGHT /2)
        #acceleration
        self.pos = vec(WIDTH /2,HEIGHT / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.dead = False

    def jump(self):
        self.vel.y = -PLAYER_JUMP

    def update(self):
        self.playing = True
        self.nabrak = False
        #acceleration
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()

        if self.playing :
            self.acc.x = -PLAYER_ACC-0.1

        self.acc.x += self.vel.x * PLAYER_FRICTION
        #acceleration / equation of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc #equation of motions, object moving around
        self.rect.midbottom = self.pos

class Player2(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/ironman (2).bmp")
        self.image = pg.transform.scale(self.image,(55 ,40))
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-10,-5)
        self.rect.center = (WIDTH /2, HEIGHT /2)
        #acceleration
        self.pos2 = vec(WIDTH /2,HEIGHT / 2)
        self.vel2 = vec(0,0)
        self.acc2 = vec(0,0)
        self.dead2 = False


    def jump(self):
        self.vel2.y = -PLAYER_JUMP


    def update(self):
        self.playing = True
        #acceleration
        self.acc2 = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()

        if self.playing :
            self.acc2.x = -PLAYER_ACCC

        self.acc2.x += self.vel2.x * PLAYER_FRICTION

        #acceleration / equation of motion
        self.vel2 += self.acc2
        self.pos2 += self.vel2 + 0.5 * self.acc2 #equation of motions,object moving around

        self.rect.midbottom = self.pos2


class Platform(pg.sprite.Sprite):

    def __init__(self, game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load("images/greenwichgraysqrect.jpg")
        self.image = pg.transform.scale(self.image,(w,h))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class FlatPlatform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load("images/greenwichgraysqrect.jpg")
        self.image = pg.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Redline(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Button():
    def __init__(self):
        self.buttons = pg.image.load("images/multi.png")
        self.buttons = pg.transform.scale(self.buttons,(100,60))
        self.buttons_rect = self.buttons.get_rect()

class Button2():
    def __init__(self):
        self.buttons = pg.image.load("images/singleplayer.png")
        self.buttons = pg.transform.scale(self.buttons,(100,55))
        self.buttons_rect = self.buttons.get_rect()

class QuitButton():
    def __init__(self):
        self.buttons = pg.image.load("images/quit.png")
        self.buttons = pg.transform.scale(self.buttons,(150,100))
        self.buttons_rect = self.buttons.get_rect()

class CloudSprite(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/cloud.png")
        self.image = pg.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class backButton():
    def __init__(self):
        self.buttons = pg.image.load("images/backMenu.png")
        self.buttons = pg.transform.scale(self.buttons,(75,50))
        self.buttons_rect = self.buttons.get_rect()
