
import pygame
import random

def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))

class FumacaWhite (pygame.sprite.Sprite):
   def __init__(self, posicao ,groups) :
      super().__init__(groups)

      #                       tamanho em pixels(4,4)
      #self.image = pygame.Surface(4,4)
      
      self.image = pygame.image.load('Asteroide/fumaca.png').convert_alpha()
      self.image = pygame.transform.scale(self.image, (100,100))
      self.image = escala(self.image, 0.1)
      self.rect = self.image.get_rect(topleft = posicao)


      """
      caso o  self.image nao preencha
      a particula com a imagem da fumaça
      self.color = "white"
      self.image.fill(self.color)
      """
      self.alpha = 255
      #define a direção da particula
      self.dir_x = 1#random.uniform(-1, 1)
      self.dir_y = 1#random.uniform(-1, 1)

   def update(self):
         
         self.rect.x += self.dir_x
         self.rect.x += self.dir_y
         self.alpha -= 5
         if self.alpha <= 0:
            self.kill()
         else:
             self.image.set_alpha(self.alpha)
         
       

      