import pygame
from pygame.locals import *
import sys
import random

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.image.load("character.png")
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.canPass = False

    def moveRelease(self, key):

        if key == pygame.K_LEFT:
            self.vel.x += 5
        elif key == pygame.K_RIGHT:
            self.vel.x -= 5
        elif key == pygame.K_DOWN:
            self.canPass = False

    def movePress(self, key):

        if key == pygame.K_LEFT:
            # self.acc.x = -ACC
            self.vel.x -= 5
        elif key == pygame.K_RIGHT:
            # self.acc.x = ACC
            self.vel.x += 5
        elif key == pygame.K_DOWN:
            self.canPass = True

    def jump(self):
        onGround = pygame.sprite.collide_rect(self, Ground)
        onPlatform = pygame.sprite.spritecollide(self, platforms, False)
        if onGround or onPlatform:
            self.vel.y = -15

    def update(self):
        gravity = 1
        self.pos += self.vel

        if self.vel.y != 10:
            self.vel.y += gravity

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

        onGround = pygame.sprite.collide_rect(self, Ground)
        onPlatform = pygame.sprite.spritecollide(self, platforms, False)

        if P1.vel.y > 0:
            if onGround:
                self.vel.y = 0
                self.pos.y = Ground.rect.top + 1
            elif onPlatform and not self.canPass:
                self.vel.y = 0
                self.pos.y = onPlatform[0].rect.top + 1

class platform(pygame.sprite.Sprite):
    def __init__(self, pos, dimentions):
        super().__init__()
        self.surf = pygame.Surface(dimentions)
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=pos)

    def move(self):
        pass


Ground = platform((WIDTH / 2, HEIGHT - 10), (WIDTH, 20))
P1 = Player()
PT1 = platform((50, HEIGHT - 100), (50, 10))


all_sprites = pygame.sprite.Group()
all_sprites.add(Ground)
all_sprites.add(P1)
all_sprites.add(PT1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                P1.jump()
            P1.movePress(event.key)
        if event.type == pygame.KEYUP:
            P1.moveRelease(event.key)

    displaysurface.fill((0, 0, 0))
    P1.update()

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)