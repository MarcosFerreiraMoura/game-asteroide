
import pygame
import random
from tiro import Tiro
pygame.init()


objectGroup = pygame.sprite.Group()
tiroGroup = pygame.sprite.Group()

def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))

class naveBoss(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image  = pygame.image.load("dados/naves/Nave_inimiga.png")
        self.image = escala(self.image, 0.6)
        self.rect = pygame.Rect(600, 200, self.image.get_width(), self.image.get_height())
        #self.rect = self.image.get_rect(midright=(800, random.randint(0, 600)))
        self.vida = 200
        self.speed = 0
        self.aceleracao = 0.1

        self.rect.x = 1000 + random.randint(1,200)
        self.rect.y =random.randint(1, 600)

        self.speed_x = random.uniform(2,-2)
        self.speed_y = random.uniform(2,-2)



    def update(self, *args):

     # Movendo suavemente
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if random.random() < 1:  #chance de mudar a direção
            self.speed_x += random.uniform(-0.5, 0.5)
            self.speed_y += random.uniform(-0.5, 0.5)
        
        # Limitando a velocidade para evitar movimentos bruscos
        self.speed_x = max(min(self.speed_x, 2), -2)
        self.speed_y = max(min(self.speed_y, 2), -2)

        self.tiros_do_boss = pygame.sprite.Group()
        if self.rect.top < 0:
            self.rect.top =  0
            self.speed = 0
        elif self.rect.bottom > 600: 
            self.rect.bottom = 600
            self.speed = 0
        if self.rect.left < 0: 
            self.rect.left = 0
        if self.rect.right > 1000:
            self.rect.right = 1000

        if self.vida <= 0:
            self.kill()


    