
import pygame
import math
from pygame.locals import*

pygame.init()
info = pygame.display.Info()

class Tiro(pygame.sprite.Sprite):
    def __init__(self, posicao, angulo, direcao, *groups):
        super().__init__(*groups)
        self.image  = pygame.image.load("assets/tiros/tiroRoxo.png")
        self.image = pygame.transform.scale(self.image, (10,10))
        self.rect = self.image.get_rect(center=posicao)

        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image, angulo)
        self.rect = self.image.get_rect(center=old_center)

        angulo_radianos = math.radians(angulo)
        speed = 4
        self.speed_x = speed * math.cos(angulo_radianos) * direcao
        self.speed_y = speed * math.sin(angulo_radianos)

    def update(self, *args):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y

        if self.rect.left > info.current_w or self.rect.top > info.current_h or self.rect.top < 0:
            self.kill()
    
    