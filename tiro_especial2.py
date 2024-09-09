import pygame
import math


class TiroEspecial(pygame.sprite.Sprite):
    def __init__(self, angulo, raio, posicao, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("game-asteroide/assets/tiros/tiroRoxo.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.image = pygame.transform.rotate(self.image, angulo)
        self.rect = self.image.get_rect(midleft=posicao)
        
        angulo_radianos = math.radians(angulo)
        self.rect.x += raio * math.cos(angulo_radianos)
        self.rect.y -= raio * math.sin(angulo_radianos)
        
        self.speed = 6
        self.speed_x = self.speed * math.cos(angulo_radianos)
        self.speed_y = self.speed * math.sin(angulo_radianos)
        self.explodiu = False

    def update(self, *args):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y

        if self.rect.left > 1000 or self.rect.bottom < 0:
            self.kill()

    def explodir(self):
        if not self.explodiu:
            self.explodiu = True
            tiros_menores = []
            for i in range(-2, 360):
                tiro_menor = TiroMenor(self.rect.centerx, self.rect.centery, i, self.groups())
                tiros_menores.append(tiro_menor)
            self.kill()
            return tiros_menores

class TiroMenor(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("assets/tiros/tiroRoxo.png")  
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = direction * 3
        self.speed_y = 3 

    def update(self, *args):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y

        if self.rect.left > 1000 or self.rect.bottom < 0:
            self.kill()