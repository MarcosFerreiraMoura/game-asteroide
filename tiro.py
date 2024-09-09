
import pygame
import math
from pygame.locals import*



class Tiro(pygame.sprite.Sprite):
    def __init__(self, angulo, raio, posicao, *groups):
        super().__init__(*groups)
        self.image  = pygame.image.load("game-asteroide/assets/tiros/tiroRoxo.png")
        self.image = pygame.transform.scale(self.image, (10,10))
        self.image = pygame.transform.rotate(self.image, angulo)
        self.rect = self.image.get_rect(midleft=posicao)

        angulo_radianos = math.radians(angulo)
        self.rect.x += raio * math.cos(angulo_radianos)
        self.rect.y -= raio * math.sin(angulo_radianos)
        
        speed = 4
        self.speed_x = speed * math.cos(angulo_radianos)
        self.speed_y = speed * math.sin(angulo_radianos)

    def update(self, *args):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y

        if self.rect.left > 1000 or self.rect.top > 600 or self.rect.top < 0:
            self.kill()
    
    