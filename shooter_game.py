from pygame import *
from random import randint
from time import time as timer



mixer.init()
mixer.music.load('kosmos.ogg')
mixer.music.play()
fire_sound = mixer.Sound('laser_shot.ogg')
crack = mixer.Sound('podbitie.mp3')



font.init()
font1 = font.SysFont('Arial', 80)
W = font1.render('STARWARS WIN', True, (128, 128, 128))
L = font1.render('UFO WIN', True, (0, 255, 0))
font2 = font.SysFont('Arial', 36)



img_enemy = 'ufo_ai.png'
img_back = 'background.jpg'
img_bullet ='laser.png'
img_hero = 'starwars.png'
img_znak = 'znak.png'


score  = 0
goal = 30
lost = 0
max_lost = 1
life = 3



class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):

        sprite.Sprite.__init__(self)



        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed



        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self): 
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 50, 70, -100)
        bullets.add(bullet)



class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1



class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()




win_width = 700
win_height = 500
display.set_caption('Star wars')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))



ship = Player(img_hero, 5, win_height - 100, 80, 100, 40)


ufo_monsters = sprite.Group()
for i in range(1, 10):
    ufo_monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 15))
    ufo_monsters.add(ufo_monster)


bullets = sprite.Group()




finish = False

run = True



rel_time = False


num_fire = 0


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:

                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False :
                    last_time = timer()
                    rel_time = True
                

    if not finish:
        window.blit(background,(0,0))

        ship.update()
        ufo_monsters.update()
        bullets.update()







        ship.reset()
        ufo_monsters.draw(window)
        bullets.draw(window)



        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload. . .', 1, (255, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        
        collides = sprite.groupcollide(ufo_monsters, bullets, True, True)
        for c in collides:

            score += 1
            ufo_monster = Enemy(img_enemy, randint(80, win_height - 80), -40, 80, 50, randint(1, 5))
            ufo_monsters.add(ufo_monster)


        if sprite.spritecollide(ship, ufo_monsters, False):
            sprite.spritecollide(ship, ufo_monsters, True)
            life -= 1

        
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(L, (200, 200))



        if score >= goal:
            finish = True
            window.blit(W, (140 ,200))



        text = font2.render('Подбито:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))


        text_lose = font2.render('Упущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        patron = font2.render('5 Лазерных патрон', 1, (0, 255, 0))
        window.blit(patron, (450, 300))



        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        if life == 0:
            crack.play()



        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))


        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in ufo_monsters:
            m.kill()


        time.delay(3000)
        for i in range(1, 10):
            ufo_monster = Enemy( img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 15))
            ufo_monsters.add(ufo_monster)
    time.delay(50)