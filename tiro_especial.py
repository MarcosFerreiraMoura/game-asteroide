import pygame
import math


pygame.init()
info = pygame.display.Info()

class TiroEspecial(pygame.sprite.Sprite):
    def __init__(self, posicao, angulo, *groups):
        super().__init__(*groups)
        #self.image = pygame.image.load("dados/tiroAzul.png")
        self.image = pygame.image.load("assets/tiros/tiroRoxo.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=posicao)
        
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image, angulo)
        self.rect = self.image.get_rect(center=old_center)
        
        self.angulo_radianos = math.radians(angulo)
        speed = 6
        
        self.speed_x = speed * math.cos(self.angulo_radianos)
        self.speed_y = speed * math.sin(self.angulo_radianos)
        self.angulo = angulo
        self.posicao = posicao
        
        self.explodiu = False

    def update(self, *args):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y

    def explodir(self):
        if not self.explodiu:
            self.explodiu = True
            tiros_menores = []
            for i in range(-4, 10, 2):
                if i == 0:
                    continue
                tiro_menor = TiroMenor((self.rect.centerx, self.rect.centery), self.angulo, self.angulo_radianos, i, self.groups())
                tiros_menores.append(tiro_menor)
            self.kill()
            return tiros_menores

class TiroMenor(pygame.sprite.Sprite):
    def __init__(self, posicao, angulo, angulo_radianos, direction, *groups):
        super().__init__(*groups)
        x, y = posicao
        #self.image = pygame.image.load("dados/tiroAzul.png")
        self.image = pygame.image.load("assets/tiros/tiroRoxo.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = pygame.transform.rotate(self.image, angulo)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = direction * 3 * math.cos(angulo_radianos)
        self.speed_y = direction * 3 * math.sin(angulo_radianos)

    def update(self, *args):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y

        if self.rect.left > info.current_w or self.rect.top > info.current_h or self.rect.top < 0:
            self.kill()