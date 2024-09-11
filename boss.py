
import pygame
import random
from tiro import Tiro


pygame.init()
info = pygame.display.Info()

objectGroup = pygame.sprite.Group()
tiroGroupBoss = pygame.sprite.Group()

def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))

class naveBoss(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.objectGroup2 = groups[0]
        self.image  = pygame.image.load("assets/naves/Nave_inimiga.png")
        self.image = escala(self.image, 0.6)
        #self.rect = pygame.Rect(info.current_h, 200, self.image.get_width(), self.image.get_height())
        self.rect = self.image.get_rect(midright=(info.current_w, info.current_h/2 + random.randint(-100,100)))
        self.vida = 200
        self.speed = 0
        self.aceleracao = 0.1

        self.speed_x = random.uniform(2,-2)
        self.speed_y = random.uniform(2,-2)

    def update(self, *args):

     # Movendo suavemente
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if random.random() < 0.5:  #chance de mudar a direção
            self.speed_x += random.uniform(-0.5, 0.5)
            self.speed_y += random.uniform(-0.5, 0.5)
        
        # Limitando a velocidade para evitar movimentos bruscos
        self.speed_x = max(min(self.speed_x, 2), -2)
        self.speed_y = max(min(self.speed_y, 2), -2)
        if self.rect.top < 0:
            self.rect.top =  0
            self.speed = 0
        elif self.rect.bottom > info.current_h: 
            self.rect.bottom = info.current_h
            self.speed = 0
        if self.rect.left < 0: 
            self.rect.left = 0
        if self.rect.right > info.current_w:
            self.rect.right = info.current_w

        if self.vida <= 0:
            self.kill()
        
        if self.alive():
            if random.random() < 0.01:
                self.atirar()
    def atirar(self):
        tiro = Tiro(self.rect.midleft, 0, -1, "redTiro", self.objectGroup2, tiroGroupBoss)

    