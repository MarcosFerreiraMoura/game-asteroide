from tiro import Tiro
from fogo import Fogo
import pygame
import math



pygame.init()
info = pygame.display.Info()

#efeitos sonoros
tiroSound = pygame.mixer.Sound("game-asteroide/assets/tiros/Fire 1.mp3")
tiroEspecialSound = pygame.mixer.Sound("game-asteroide/assets/tiros/Fire 5.mp3")
tiroMenorSound = pygame.mixer.Sound("game-asteroide/assets/tiros/Fire 3.mp3")

tiroGroup = pygame.sprite.Group()

tiro_especial = None

def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))

class Foguete(pygame.sprite.Sprite):
    def __init__(self, objectGroup1, *groups):
        super().__init__(*groups)
        self.objectGroup1 = objectGroup1
        self.objectGroup2 = groups[0]
        
        self.img  = pygame.image.load("game-asteroide/assets/naves/po.png")
        self.img = escala(self.img, 0.6)
        self.image = self.img
        self.raio = self.image.get_width() / 2
        self.rect = self.image.get_rect(center=(50, 50))
        self.angulo = 0
        self.newFogo = Fogo(self.objectGroup1) #nivel1 na textura
        self.timer = 0
        

    def update(self, *args):
        eventos = args[0]
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                self.timer = 0
                tiroSound.play()
                newTiro = Tiro(self.angulo, self.raio, self.rect.center, self.objectGroup2, tiroGroup)
            
        
        keys  = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not (self.timer % 10):
            tiroSound.play()
            newTiro = Tiro(self.angulo, self.raio, self.rect.center, self.objectGroup2, tiroGroup)
        if keys[pygame.K_a]:
            self.rect.x -= 2
        elif keys[pygame.K_d]:
            self.rect.x += 2
        if keys[pygame.K_w]:
            self.rect.y -=2
            self.angulo = 10
        elif keys[pygame.K_s]:
            self.angulo = -10
            self.rect.y += 2
        else:
            self.angulo = 0
        
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.img, self.angulo)
        self.rect = self.image.get_rect(center=old_center)
        
        if self.rect.top < 0:
            self.rect.top =  0
            self.speed = 0
        elif self.rect.bottom > info.current_h: 
            self.rect.bottom = info.current_h
            self.speed = 0
        if self.rect.left < 0: 
            self.rect.left = 0
        
        self.timer += 1
        angulo_rad = math.radians(self.angulo)
        posicao_fogo = list(self.rect.center)
        posicao_fogo[0] -= (self.raio * 0.8) * math.cos(angulo_rad)
        posicao_fogo[1] += (self.raio * 0.8) * math.sin(angulo_rad) - 1
        self.newFogo.update(posicao_fogo, self.angulo) #posição, angulo