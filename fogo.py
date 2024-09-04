import pygame
import random
import math

fogoGroup = pygame.sprite.Group()

def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))

class ParticulaFogo(pygame.sprite.Sprite):
  def __init__(self, pos, offset_aleatorio, *groups):
    super().__init__(*groups)
    self.img = pygame.image.load('dados/imagens/fogos/fogo1.png').convert_alpha()
    self.img = escala(self.img, 0.13)
    self.image = self.img
    self.rect = self.image.get_rect(center = pos)
    self.alpha = 255
    self.image.set_alpha(self.alpha)
    self.aleatorio_x, self.aleatorio_y = offset_aleatorio
    
    self.offset_x = 0
    self.offset_y = 0
    
    self.rect.x -= self.offset_x + self.aleatorio_x
    self.rect.y += self.offset_y + self.aleatorio_y
    self.timer = 0
  
  def update(self, *args): #posição, angulo
    if not len(args):
      return

    if self.timer >= 60:
      self.timer = 0
    self.timer += 1
    
    #definindo variáveis
    self.rect.center = args[0] if len(args) > 0 else self.rect.center
    angulo = args[1] if len(args) > 0 else 0
    
    #ajustando posição e angulo
    old_center = self.rect.center
    self.image = pygame.transform.rotate(self.img, angulo)
    self.rect = self.image.get_rect(center=old_center)
    
    angulo_rad = math.radians(angulo)

    self.offset_x += math.cos(angulo_rad) * 0.5
    self.offset_y += math.sin(angulo_rad) * 0.5
    
    if (self.offset_x * math.cos(angulo_rad) + self.offset_y * math.sin(angulo_rad)) > 15:
      self.kill()
    
    self.rect.x -= self.offset_x + self.aleatorio_x
    self.rect.y += self.offset_y + self.aleatorio_y
    
    self.alpha -= 10
    if self.alpha <= 0:
      self.kill()
    else:
      self.image.set_alpha(self.alpha)
    
    if not self.timer % 60:
      self.kill()

class Fogo:
  def __init__(self, *groups):
    self.objectGroup1 = groups[0]
    self.timer = 0
    self.direcao = 2
  
  def update(self, *args):
    if not len(args):
      return
    pos, angulo = args
    
    angulo_rad = math.radians(angulo)
    fogoGroup.update(pos, angulo)
    if not self.timer % 7:
      self.direcao *= -1
      offset_aleatorio_x, offset_aleatorio_y = self.direcao * math.sin(angulo_rad), self.direcao * math.cos(angulo_rad)
      newParticulaFogo = ParticulaFogo(pos, (offset_aleatorio_x, offset_aleatorio_y), self.objectGroup1, fogoGroup)

    if self.timer >= 60:
      self.timer = 0
    self.timer += 1
