import pygame
import math


pygame.init()
info = pygame.display.Info()

def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))

class TiroEspecial(pygame.sprite.Sprite):
    def __init__(self, posicao, angulo, *groups):
        super().__init__(*groups)
        #self.image = pygame.image.load("dados/tiroAzul.png")
        self.image = pygame.image.load("assets/tiros/tiroAzul.png")
        self.image = escala(self.image, 1)
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
            for i in range(-45, 45, 15):
                offset_angulo = self.angulo + i
                offset_angulo_radianos = math.radians(offset_angulo)
                tiro_menor = TiroMenor((self.rect.centerx, self.rect.centery), offset_angulo, offset_angulo_radianos, self.groups())
                tiros_menores.append(tiro_menor)
            self.kill()
            return tiros_menores

class TiroMenor(pygame.sprite.Sprite):
    def __init__(self, posicao, angulo, angulo_radianos, *groups):
        super().__init__(*groups)
        x, y = posicao
        #self.image = pygame.image.load("dados/tiroAzul.png")
        self.image = pygame.image.load("assets/tiros/tiroAzul.png")
        self.image = escala(self.image, 0.5)
        self.image = pygame.transform.rotate(self.image, angulo)
        
        self.alpha = 255
        self.image.set_alpha(self.alpha)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 6 * math.cos(angulo_radianos)
        self.speed_y = 6 * math.sin(angulo_radianos)

    def update(self, *args):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y
        
        self.alpha -= 2
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)

        if not (0 < self.rect.left < info.current_w) or not (0 < self.rect.top < info.current_h):
            self.kill()