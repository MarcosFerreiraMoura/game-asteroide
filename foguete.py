
import pygame
pygame.init()

def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))

class Foguete(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image  = pygame.image.load("dados/naves\po.png")
        self.image = escala(self.image, 0.6)
        self.rect = pygame.Rect(50, 50, self.image.get_width(), self.image.get_height())

        self.speed = 0
        self.aceleracao = 0.1

    def update(self, *args):
        keys  = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= 2
        elif keys[pygame.K_d]:
            self.rect.x += 2
        if keys[pygame.K_w]:
             self.rect.y -=2
        elif keys[pygame.K_s]:
             self.rect.y += 2
        else:
            self.speed  *= 0.85
        self.rect.y += self.speed
        self.rect.x += self.speed

        if self.rect.top < 0:
            self.rect.top =  0
            self.speed = 0
        elif self.rect.bottom > 600: 
            self.rect.bottom = 600
            self.speed = 0
        if self.rect.left < 0: 
            self.rect.left = 0

        return super().update(*args)