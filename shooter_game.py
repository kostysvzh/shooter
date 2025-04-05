from pygame import *
import random

mixer.init()

window = display.set_mode((700, 500))
win_w = 700
win_h = 500
display.set_caption('shooter')
bg = transform.scale(image.load('galaxy.jpg'), (win_w, win_h))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()




lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.x = random.randint(80,win_w - 80)
            self.rect.y = 0
            lost = lost + 1

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_h:
            self.rect.x = random.randint(80,win_w - 80)
            self.rect.y = 0
            

player = Player('rocket.png', 5, win_h - 80, 80, 100, 10)
enemies = sprite.Group()
meteors = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', random.randint(0, win_w - 80), random.randint(-100, 0), 80, 50, 2)
    enemies.add(enemy)

for i in range(1):
    meteor = Meteor('asteroid.png', random.randint(0, win_w - 80), random.randint(-100, 0), 80, 50, 2)
    meteors.add(meteor)

game = True
clock = time.Clock()

mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)

font.init()
font2 = font.SysFont('Arial', 40)
font1 = font.SysFont('Arial', 70)
win = font1.render('YOU WIN!',True,(0,255,0))
lose = font1.render('YOU LOSE!',True,(255,0,0))


bullets = sprite.Group()
shots_fired = 0
reloading = False
reload_time = 3000
last_shot_time = 0
score = 0


def fire():
    global shots_fired, reloading, last_shot_time
    if not reloading:
        bullet = Bullet('bullet.png', player.rect.centerx - 10, player.rect.top, 20, 40, 10)
        bullets.add(bullet)
        shots_fired += 1
        if shots_fired >= 5:
            reloading = True
            last_shot_time = time.get_ticks()

finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:  
                fire()
                

    if not finish:
        window.blit(bg, (0, 0))
        player.reset()
        player.update()
        enemies.draw(window)  
        enemies.update() 
        bullets.update()
        bullets.draw(window)
        meteors.update()
        meteors.draw(window)
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 0, 0))
        window.blit(text_lose, (10, 10))
        text_scr = font2.render('Очки:' + str(score), 1, (255, 0, 0))
        window.blit(text_scr, (10, 100))

        if reloading:
            current_time = time.get_ticks()
            if current_time - last_shot_time >= reload_time:
                reloading = False
                shots_fired = 0
            reload_text = font2.render('Перезарядка...', 1, (255, 255, 0))
            window.blit(reload_text, (10, 50))

        if lost > 2:
            finish = True
            window.blit(lose, (200,200))

        if sprite.spritecollide(player,enemies, True):
            finish = True
            window.blit(lose, (200,200))

        if sprite.spritecollide(player,meteors, True):
            finish = True
            window.blit(lose, (200,200))

        if sprite.groupcollide(enemies,bullets,True,True):
            score += 1
            enemy = Enemy('ufo.png', random.randint(0, win_w - 80), random.randint(-100, 0), 80, 50, 1)
            enemies.add(enemy)
        if score > 9:
            finish = True
            window.blit(win, (200,200))

    display.update()
    time.delay(10)
    
