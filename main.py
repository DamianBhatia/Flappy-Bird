import pygame
import sys
import random


class Pipe:
    def __init__(self, x, y, w, h, screen):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.screen = screen
        self.cooldown = 50
        self.last = pygame.time.get_ticks()
        self.pipe_img = pygame.image.load('pipe.png')
        self.rect1 = pygame.Rect(self.x, self.h-400, self.w, self.h)
        self.rect2 = pygame.Rect(self.x, self.h+160, self.w, 500)

    def render(self):
        self.rect1 = pygame.Rect(self.x, self.h-400, self.w, self.h)
        self.rect2 = pygame.Rect(self.x, self.h+160, self.w, 500)

        self.screen.blit(pygame.transform.flip(self.pipe_img, False, True), self.rect1)
        self.screen.blit(self.pipe_img, self.rect2)
        # pygame.draw.rect(self.screen, (64, 179, 63), rect1)
        # pygame.draw.rect(self.screen, (64, 179, 63), rect2)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            self.x -= 5


class Player:
    def __init__(self, x, y, color, width, screen):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.screen = screen
        self.jumpCount = 10
        self.isJump = False
        self.bird = pygame.image.load('bird.png')
        self.rect = pygame.Rect(self.x, int(self.y), self.width*2, self.width*2)

    def render(self):
        self.rect = pygame.Rect(self.x, int(self.y), self.width*2, self.width*2)
        self.screen.blit(self.bird, self.rect)

    def update(self):
        if self.jumpCount >= 0:
            self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.35
            self.jumpCount -= 1
        else:
            self.jumpCount = 10
            self.isJump = False


pygame.init()
screen = pygame.display.set_mode((300, 500))
running = True
player = Player(50, 250, (255, 229, 0), 15, screen)
fall_cd = 3
jump_cd = 30
last_fall = pygame.time.get_ticks()
last_jump = pygame.time.get_ticks()
pipes = [Pipe(270, 0, 70, 130, screen)]
background_img = pygame.image.load('background.png')
score = 0

while running:

    if player.y >= 500:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        player.isJump = True
    else:
        curr_fall = pygame.time.get_ticks()
        if curr_fall - last_fall >= fall_cd:
            last_fall = curr_fall
            player.y += 1.2

    if player.isJump:
        curr_jump = pygame.time.get_ticks()
        if curr_jump - last_jump >= jump_cd:
            last_jump = curr_jump
            player.update()

    screen.fill((192, 234, 246))
    screen.blit(background_img, (0,0))
    player.render()

    for pipe in pipes:
        if player.rect.colliderect(pipe.rect1) or player.rect.colliderect(pipe.rect2):
            running = False
        if pipe.x <= -70:
            score += 1
            pipes.remove(pipe)
        elif pipes[-1].x < 300:
            pipes.append(Pipe(random.randint(500, 551), 0, 70, random.randint(50, 375), screen))
        else:
            pipe.update()
            pipe.render()


    myfont = pygame.font.SysFont("Comic Sans MS", 20)
    label = myfont.render("SCORE: " + str(score), 1, (0, 0, 0))
    screen.blit(label, (200, 5))

    pygame.display.flip()
