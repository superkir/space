import pygame
from random import randint

pygame.init()

FPS = 70
clock = pygame.time.Clock()
#створи вікно гри

wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w, wind_h))
pygame.display.set_caption("Shooter")

#завантаження музики
pygame.mixer.music.load("space1.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

fire_snd = pygame.mixer.Sound("fire.ogg")


#задай фон сцени
background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (wind_w, wind_h))

background1 = pygame.image.load("space1.png")
background1 = pygame.transform.scale(background1, (wind_w, wind_h))

class Sprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self, a, d):
        keys = pygame.key.get_pressed()
        if keys[a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[d]:
            if self.rect.right < wind_w:
                self.rect.x += self.speed

    def fire(self):
        bullets.append(Bullet(self.rect.centerx - 13, self.rect.y, 25, 50, bullet_img, 15))
        fire_snd.play()

class Enemy(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self):
        global lost_lb, lost
        self.rect.y += self.speed
        if self.rect.y >= wind_h:
            self.rect.x = randint(0, wind_w-self.rect.w)
            self.rect.y = randint(-250, -50)
            lost += 1
            lost_lb = font_stat.render(f"пропущенно: {lost}", True, (255, 255, 255))
            

class Bullet(Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            bullets.remove(self)

player = Player(0, 400, 50, 50, pygame.image.load("rocket.png"), 15)

enemy_img = pygame.image.load("ufo.png")
enemies = []

bullet_img = pygame.image.load("bullet.png")
bullets = []
for i in range(10):
    enemies.append(Enemy(randint(0, wind_w-70), randint(-250, -50), 70, 50, enemy_img, 4))


#lose = font.render("You Lose!", True, (0, 0, 250))
#win = font.render("You Win!", True, (150, 100, 200))
#lose1 = font1.render("Press SPACE to play again", True, (255, 255, 102))
#win1 = font1.render("Press SPACE to play again", True, (255, 255, 102))

points = 0
lost = 0
font = pygame.font.SysFont("Arial", 80)
font_stat = pygame.font.SysFont("Arial", 30)
points_lb = font_stat.render(f"вбито: {points}", True,(255, 255, 255))
lost_lb = font_stat.render(f"пропущенно: {lost}", True, (255, 255, 255))

but_img = pygame.image.load("button.png")
button = Sprite(200, 200, 200, 50, but_img)

finish = False
game = True
menu = True

while game:
    if menu:
        window.blit(background1, (0, 0))
        button.draw()

    pygame.display.update()
    clock.tick(FPS)
    if not finish and not menu:
        window.blit(background, (0, 0))
        window.blit(points_lb, (0, 0))
        window.blit(lost_lb, (0, 50))

        for enemy in enemies:
            enemy.draw()
            enemy.move()
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    enemy.rect.x = randint(0, wind_w-enemy.rect.w)
                    enemy.rect.y = randint(-250, -50)
                    bullets.remove(bullet)
                    points += 1
                    points_lb = font_stat.render(f"вбито: {points}", True,(255, 255, 255))
                    

        for bullet in bullets:
            bullet.draw()
            bullet.move()
            
        player.draw()
        player.move(pygame.K_a, pygame.K_d)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.fire()
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
           #player = Player(0, 400, 50, 50, pygame.image.load("sprite1.png"), 5)
            #finish = False
        if menu and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y, = event.pos 
            if button.rect.collidepoint(x, y):
                menu = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("space.ogg")
                pygame.mixer.music.play(-1)

    pygame.display.update()
    clock.tick(FPS)