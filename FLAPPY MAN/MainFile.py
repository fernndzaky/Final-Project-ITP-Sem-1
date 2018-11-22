import pygame as pg
import random
from SpritesFile import *
from SettingsFile import *


class Game():
    def __init__(self):
        #initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.rand = random.randrange(100,350)
        self.main = True
        self.multiplayer = False
        self.menu = False
        self.highscore = 0

    def saveData(self):
        file = open("highscore.txt","w")
        a = str(self.highscore)
        file.write(a)
        file.close()

    def loadData(self):
        file = open("highscore.txt","r")
        for i in file:
            self.highscore = int(i)

    def new(self):
        # Create / Start a  New Game
        self.paused = True
        self.score = 0
        self.score2 = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.redlines = pg.sprite.Group()
        self.flatPlatforms = pg.sprite.Group()
        self.cloudGroup = pg.sprite.Group()
        self.player = Player()
        self.player2 = Player2()
        if not self.multiplayer:
            self.all_sprites.add(self.player)
        if self.multiplayer:
            self.all_sprites.add(self.player)
            self.all_sprites.add(self.player2)
        for plat in PLATFORM_LIST :
            p = Platform(self,*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for line in REDLINE_LIST:
            r = Redline(*line)
            self.all_sprites.add(r)
            self.redlines.add(r)
        for lines in FLATPLAT_LIST:
            f = FlatPlatform(self,*lines)
            self.all_sprites.add(f)
            self.flatPlatforms.add(f)
        for line in CLOUD_LIST:
            f = CloudSprite(*line)
            self.all_sprites.add(f)
            self.cloudGroup.add(f)
        g.run()

    def run(self):
        # Game Loop
        self.playing = True

        while self.playing :
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        # Game Loop - Update

        self.all_sprites.update()
        self.rand = random.randrange(100,350)
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        hits2 = pg.sprite.spritecollide(self.player2, self.platforms, False)
        if not self.multiplayer:
            if hits:
                if not self.player.dead:
                    self.hitSound()
                    self.main = False
                    self.player.dead = True
                    self.player.vel.x = 0

        if self.multiplayer:
            if hits2:
                if not self.player2.dead2:
                    self.hitSound()
                    self.main = False
                    self.player2.dead2 = True
                    self.player2.vel2.x = 0

            if hits:
                if not self.player.dead:
                    self.hitSound()
                    self.main = False
                    self.player.dead = True
                    self.player.vel.x = 0

        if not self.multiplayer:
            if self.player.rect.y > HEIGHT :
                self.player.dead = True
                self.playing = False

            if self.player.rect.y < 0 :
                if not self.player.dead:
                    self.hitSound()
                    self.main = False
                    self.player.dead = True
                    self.player.vel.x = 0

        if self.multiplayer:
            if self.player.rect.y < 0:
                if not self.player.dead:
                    self.hitSound()
                    self.main = False
                    self.player.dead = True
                    self.player.vel.x = 0

            if self.player2.rect.y < 0:
                if not self.player2.dead2 :
                    self.hitSound()
                    self.main = False
                    self.player2.dead2 = True
                    self.player2.vel2.x = 0


            if self.player.rect.y > HEIGHT and self.player2.rect.y > HEIGHT:
                self.playing = False

            if self.player2.rect.y > HEIGHT :
                self.player2.dead2 = True
                self.player2.kill()


            if self.player.rect.y > HEIGHT :
                self.player.dead = True
                self.player.kill()

            if not self.playing and self.main:
                self.hitSound()

        if not self.playing and self.main:
            self.hitSound()

        hitred1 = pg.sprite.spritecollide(self.player, self.redlines, True)
        hitred2 = pg.sprite.spritecollide(self.player2, self.redlines, True)
        if hitred1 and not self.multiplayer :
            if not self.player.dead:
                self.score += 1
                self.scoreSound()

        if self.multiplayer:
            if hitred2 or hitred1:
                if not self.player2.dead2 and not self.player.dead:
                    self.score2 += 1
                    self.score += 1
                    self.scoreSound()
            if hitred1 or hitred2:
                if not self.player.dead and self.player2.dead2 :
                    self.score +=1
                    self.scoreSound()
            if hitred1 or hitred2:
                if self.player.dead and not self.player2.dead2 :
                    self.score2 +=1
                    self.scoreSound()

        # if player reaches 1/2 of screen
        if self.player.rect.x <= WIDTH/2 :
            #biar dia stop di tengah
            self.player.pos.x = WIDTH/2
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)
            #abs = round up

                # to delete the plat that already passed
                if plat.rect.x >= WIDTH:
                    plat.kill()
            for red in self.redlines:
                red.rect.x += abs(self.player.vel.x)
                if red.rect.x >= WIDTH:
                    red.kill()
            for cloud in self.cloudGroup:
                cloud.rect.x += abs(self.player.vel.x)
                if cloud.rect.x >= WIDTH:
                    cloud.kill()

        if self.player2.rect.x <= WIDTH/2 :
            self.player2.pos2.x += abs(self.player2.vel2.x)
            for plat in self.platforms:
                plat.rect.x += abs(self.player2.vel2.x)
                # to delete the plat that already passed
                if plat.rect.x >= WIDTH:
                    plat.kill()
            for red in self.redlines:
                red.rect.x += abs(self.player2.vel2.x)
                if red.rect.x >= WIDTH:
                    red.kill()

        #spawn new platforms to keep same average number
        while len(self.platforms) < 3 and len(self.redlines) < 3 and len(self.cloudGroup) < 3:

            x = random.randrange(50,350)
            p = Platform(self,0,0,40,x)
            p1 = Platform(self,0,x+150,40,500)
            pf2 = FlatPlatform(self,0,560,480,40)
            rl = Redline(0, 0, 0, 800)
            c = CloudSprite(random.randrange(0,100),random.randrange(10,100),200,150)
            self.cloudGroup.add(c)
            self.flatPlatforms.add(pf2)
            self.redlines.add(rl)
            self.platforms.add(p)
            self.platforms.add(p1)
            self.all_sprites.add(c)
            self.all_sprites.add(p)
            self.all_sprites.add(p1)
            self.all_sprites.add(rl)
            self.all_sprites.add(pf2)


    def events(self):
        # Game Loop - Update
        for event in pg.event.get():
            #checking for closing window
            if event.type == pg.QUIT:
                if self.playing :
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if not self.player.dead and not self.multiplayer:
                    if event.key == pg.K_SPACE:
                        self.paused = False
                        self.jumpSound()
                        self.player.jump()

                if not self.player2.dead2 and self.multiplayer :
                     if event.key == pg.K_a:
                        self.paused = False
                        self.jumpSound()
                        self.player2.jump()
                if not self.player.dead and self.multiplayer:
                     if event.key == pg.K_SPACE:
                        self.paused = False
                        self.jumpSound()
                        self.player.jump()


    def jumpSound(self):
        jump = pg.mixer.Sound("sound/small_jump.ogg")
        jump.play()

    def hitSound(self):
        dead = pg.mixer.Sound("sound/death.ogg")
        dead.play()

    def scoreSound(self):
        score = pg.mixer.Sound("sound/sfx_point.wav")
        score.play()

    def draw(self):
        # Game Loop - Draw
        self.screen.fill(LIGHTBLUE)
        self.all_sprites.draw(self.screen)
        if not self.multiplayer:
            if not self.paused :
                self.draw_text(str(self.score),60,WHITE,WIDTH/2,40)
        if self.multiplayer :
            if not self.paused:
                self.draw_text("P 2 : "+str(self.score2),40,WHITE,WIDTH/2+150,40)
                self.draw_text("P 1 : "+str(self.score),40,WHITE,WIDTH/2-150,40)
        #after drawing everything , flip the display
        pg.display.flip()
        if self.paused:
            if not self.multiplayer:
                self.draw_text("Press Space To Jump",22,WHITE,WIDTH/2,HEIGHT*3/4)
                pg.display.flip()
            if self.multiplayer:

                self.draw_text("Player 1 ( Man )    : Press Space To Jump",22,WHITE,WIDTH/2,HEIGHT*3/4)
                self.draw_text("Player 2 ( Iron Man ) : Press A To Jump",22,WHITE,WIDTH/2,HEIGHT*3/4+30)
                #self.draw_text("Press Space or A To Play",22,WHITE,WIDTH/2,HEIGHT*3/4-30)
                pg.display.flip()


    def show_start_screen(self):
        # game splash/start screen
        self.menu = True
        mouse = pg.mouse.get_pos()
        self.screen_rect = self.screen.get_rect()
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE,48,WHITE,WIDTH/2,HEIGHT/4)
        self.draw_text("Jump and Evade The Walls !",22,WHITE,WIDTH/2,HEIGHT/2)

        self.button = Button()
        self.button2 = Button2()

        self.button.buttons_rect.centerx = 300
        self.button.buttons_rect.centery = 370
        self.screen.blit(self.button.buttons, self.button.buttons_rect)

        self.button2.buttons_rect.centerx = 170
        self.button2.buttons_rect.centery = 370
        self.screen.blit(self.button2.buttons, self.button2.buttons_rect)

        self.quitButton = QuitButton()
        self.quitButton.buttons_rect.centerx = 240
        self.quitButton.buttons_rect.centery = 450
        self.screen.blit(self.quitButton.buttons, self.quitButton.buttons_rect)

        self.backButtons = backButton()

        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        #kalo di keluarin gamenya biar gak ke gameover screen pake ini
        if not self.running:
            return
        self.menu = False

        #game over/continue
        if not self.multiplayer:
            self.screen.fill(BGCOLOR)
            self.draw_text("Game Over",48,WHITE,WIDTH/2,HEIGHT/4)
            self.draw_text("Score : "+ str(self.score) ,22,WHITE,WIDTH/2,HEIGHT/2)
            self.draw_text("Press  Return Key To Play Again",22,WHITE,WIDTH/2,HEIGHT*3/4)

        if self.multiplayer :
            self.screen.fill(BGCOLOR)
            self.draw_text("Game Over",48,WHITE,WIDTH/2,HEIGHT/4)
            if self.score == self.score2 :
                self.draw_text("It's A DRAW !",30,WHITE,WIDTH/2,HEIGHT/2-50)
            if self.score > self.score2:
                self.draw_text("Player 1 WIN !",30,WHITE,WIDTH/2,HEIGHT/2-50)
            if self.score2 > self.score :
                self.draw_text("Player 2 WIN !",30,WHITE,WIDTH/2,HEIGHT/2-50)
            self.draw_text("Score Player 2 : "+ str(self.score2) ,22,WHITE,WIDTH/2+100,HEIGHT/2+90)
            self.draw_text("Score Player 1 : "+ str(self.score) ,22,WHITE,WIDTH/2-100,HEIGHT/2+90)
            self.draw_text("Press  Return Key To Play Again",22,WHITE,WIDTH/2,HEIGHT*3/4)

        if not self.multiplayer:
            if self.score > self.highscore:
                self.highscore = self.score
                self.draw_text("Congratulations, You Beat The Highscore",22,WHITE,WIDTH/2,HEIGHT/2+40)
                g.saveData()

            else :
                self.draw_text("High Score : "+ str(self.highscore),22,WHITE, WIDTH/2,HEIGHT/2 + 40 )

        if self.multiplayer:
            if self.score > self.highscore:
                self.highscore = self.score
                self.draw_text("Congratulations, You Beat The Highscore",22,WHITE,WIDTH/2,HEIGHT/2+40)
                g.saveData()


            elif self.score2 > self.highscore:
                self.highscore = self.score2
                self.draw_text("Congratulations, You Beat The Highscore",22,WHITE,WIDTH/2,HEIGHT/2+40)
                g.saveData()

            else :
                self.draw_text("High Score : "+ str(self.highscore),22,WHITE, WIDTH/2,HEIGHT/2 + 40 )


        self.backButtons.buttons_rect.centerx = 240
        self.backButtons.buttons_rect.centery = 500
        self.screen.blit(self.backButtons.buttons, self.backButtons.buttons_rect)
        pg.display.flip()
        self.wait_for_key()

    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface,text_rect)



    def wait_for_key(self):
        global waiting
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False


                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN :
                        waiting = False
                        pg.mixer.pause()

                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x,mouse_y = pg.mouse.get_pos()
                    if self.menu:

                        self.checkMouse(mouse_x,mouse_y)
                        if flag == 1:
                            waiting = False

                        self.checkMouse2(mouse_x,mouse_y)
                        if flag2 == 1:
                            waiting = False

                        self.checkQuit(mouse_x,mouse_y)
                        if flag3 == 1:
                            waiting = False
                            self.running = False

                    self.backMenu(mouse_x, mouse_y)
                    if flag4 == 1:
                        g.show_start_screen()

    def backMenu(self, mouse_x , mouse_y):
        global flag4
        flag4 = 0
        button_clicked = self.backButtons.buttons_rect.collidepoint(mouse_x,mouse_y)
        if button_clicked :
            flag4 = 1
            pg.mixer.pause()
        return flag4

    def checkMouse(self, mouse_x, mouse_y):
        global flag
        flag = 0
        button_clicked = self.button.buttons_rect.collidepoint(mouse_x,mouse_y)
        if button_clicked :
            self.multiplayer = True
            flag = 1
            pg.mixer.pause()
        return flag

    def checkMouse2(self, mouse_x , mouse_y):
        global flag2
        flag2 = 0
        button_clicked = self.button2.buttons_rect.collidepoint(mouse_x,mouse_y)
        if button_clicked:
            self.multiplayer = False
            flag2 = 1
            pg.mixer.pause()
        return flag2

    def checkQuit(self, mouse_x , mouse_y):
        global flag3
        flag3 = 0
        button_clicked = self.quitButton.buttons_rect.collidepoint(mouse_x,mouse_y)
        if button_clicked :
            flag3 = 1
        return flag3

g = Game()
g.show_start_screen()
try :
    g.loadData()
except:
    if IndexError:
        g.saveData()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()


