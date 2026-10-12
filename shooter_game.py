#Create your own shooter

from pygame import *
from random import randint

screenwidth = 700
screenheight = 500
screensize = (screenwidth,screenheight)
window = display.set_mode(screensize)
display.set_caption("shooter")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image =transform.scale(image.load(player_image), (player_width,player_height))
        self.speed =player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys =key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < screenwidth - 70:
            self.rect.x += self.speed


    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > screenheight:
            self.rect.x = randint(55,screenwidth - 70)
            self.rect.y = -50
            miss += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player("rocket.png", 100, screenheight - 50, 80, 100, 5 )
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", randint(55, screenwidth - 70), -50, 80, 100, randint(1,6))
    enemies.add(enemy)
bullets = sprite.Group()

background = transform.scale(image.load('galaxy.jpg'), screensize)
FPS = 60
clock = time.Clock()
running = True
finish = False

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(5)
fire_sound = mixer.Sound("fire.ogg")

font.init()
text = font.Font(None, 30) 
end_text = font.Font(None, 80)
lose_page = end_text.render('YOU LOSE!', True, (180, 0, 0))
win_page = end_text.render('YOU WIN!', True, (0, 180, 0) )
score = 0
miss = 0


while running:
    for ev in event.get():
        if ev.type == QUIT:
            running = False
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        window.blit(background, (0,0))
        ship.update()
        ship.reset()
        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)

        collisions = sprite.groupcollide(enemies, bullets,True,True)
        for collision in collisions:
            score += 1
            enemy = Enemy('ufo.png', randint(55, screenwidth-70), -50, 80, 100, randint(1,6))
            enemies.add(enemy)

        if sprite.spritecollide(ship, enemies, False) or miss >= 3:
            finish = True
            window.blit (lose_page, (200, 200))

        if score >= 10:
            finish = True
            window.blit(win_page, (200, 200))

        hit = text.render("score: "+ str(score),1, (255, 255,255))
        window.blit(hit, (10,20))

        missed = text.render("missed: "+ str(miss),1, (255,255,255))
        window.blit(missed, (600,20))
       
    display.update()
    clock.tick(FPS)