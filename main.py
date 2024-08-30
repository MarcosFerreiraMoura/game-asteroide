import pygame
import math
import random



screen_width = 752
screen_height = 656

screen = pygame.display.set_mode((screen_width, screen_height))
IMAGEM_FUMACA = pygame.image.load('fumaca.png')


clock = pygame.time.Clock()
FPS = 60
def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))
def modulo(n):
  if n < 0:
    return -n
  else:
    return n
def nao_modulo(n):
  if n < 0:
    return n
  else:
    return -n
  
class ParticulaFumaca:
  def __init__(self, x=screen_width // 2, y=screen_height // 2):
    self.x = x
    self.y = y
    self.escala = 0.024
    self.img = escala(IMAGEM_FUMACA, self.escala)
    self.opacidade = 200
    self.taxa_crescimento = 1 #tamanho tem relação com a transparência
    self.viva = True
    self.massa = 1
    self.velocidade_x_inicial = random.random()*random.choice([-1, 1])
    self.velocidade_y_inicial = 5 + random.randint(7, 10) / 10
    self.velocidade_x = self.velocidade_x_inicial
    self.velocidade_y = self.velocidade_y_inicial
    self.tempo = 1 / FPS
    self.gravidade = 0.1
    self.forca_gravidade_y = self.gravidade * self.massa
    self.forca_reacao_y = 0
    self.aceleracao_reacao_y = 0
    self.aceleracao_gravidade = self.forca_gravidade_y / self.massa
    self.fator_resistencia_ar_y = 0.5
    self.forca_resistencia_ar_y = 0
    self.aceleracao_resistencia_ar_y = 0
    self.aceleracao_y = 0
    self.aceleracao_x = 0

  def update(self):
    self.forca_resistencia_ar_y = self.fator_resistencia_ar_y * self.velocidade_y
    self.aceleracao_resistencia_ar_y = self.forca_resistencia_ar_y / self.massa
    
    self.aceleracao_reacao_y = self.forca_reacao_y / self.massa
    
    self.aceleracao_y = self.aceleracao_gravidade - self.aceleracao_resistencia_ar_y - self.aceleracao_reacao_y
    
    self.velocidade_x = self.velocidade_x_inicial + self.aceleracao_x * self.tempo
    self.velocidade_y = self.velocidade_y_inicial + self.aceleracao_y * self.tempo

    self.escala += 0.002 * self.taxa_crescimento
    self.opacidade -= 1 * self.taxa_crescimento
    
    self.velocidade_x_inicial = self.velocidade_x
    self.velocidade_y_inicial = self.velocidade_y
    
    if self.opacidade < 0:
        self.opacidade = 0
        self.viva = False
    if self.y > 1.5*screen_height:
      self.forca_reacao_y = self.massa * self.gravidade * 2
      self.velocidade_y_inicial = 0
    
    self.x += self.velocidade_x
    self.y += self.velocidade_y
    
    self.img = escala(IMAGEM_FUMACA, self.escala)
    self.img.set_alpha(self.opacidade)
    
  def draw(self, camera_offset_x, camera_offset_y):
    screen.blit(self.img, self.img.get_rect(center=(self.x + camera_offset_x, self.y + camera_offset_y)))

class Fumaca:
  def __init__(self):
    self.particulas = []
    self.x = 0
    self.y = 0
    self.tempo = 0
  
  def add(self, x, y):
    self.x = x
    self.y = y
    if self.tempo % 2 == 0:
        self.tempo = 0
        self.particulas.append(ParticulaFumaca(self.x, self.y))
    self.tempo += 1
  
  def update(self):
    self.particulas = [i for i in self.particulas if i.viva]
    for p in self.particulas:
      p.update()
  
  def draw(self, camera_offset_x, camera_offset_y):
    for p in self.particulas:
      p.draw(camera_offset_x, camera_offset_y)

class Foguete:
  def __init__(self, x=screen_width / 2, y = screen_height):
    self.img = escala(IMAGEM_FOGUETE, 0.1)
    self.angulo = 45
    self.x = x
    self.y = y
    self.massa = 10000
    self.forca_propulsao = 0
    self.forca_propulsao_x = 0
    self.forca_propulsao_y = 0
    self.aceleracao_propulsao_x = 0
    self.aceleracao_propulsao_y = 0
    self.velocidade_y_inicial = 0
    self.velocidade_x_inicial = 0
    self.velocidade_y = 0
    self.velocidade_x = 0
    self.tempo = 1/FPS
    self.gravidade = 10
    self.aceleracao_angular_lateral = 0
    self.posicao_inicial_x = 0
    self.posicao_inicial_y = 0
    self.posicao_x = 0
    self.posicao_y = 0
    self.angulo_direcao = 0
    self.camera_offset_x = 0
    self.camera_offset_y = 0
    self.fumaca = Fumaca()
  
  def update(self):
    keys_pressed = pygame.key.get_pressed()
    angulo_radianos = math.radians(self.angulo + 45)
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_RIGHT]:
      if keys_pressed[pygame.K_LEFT]:
        self.aceleracao_angular_lateral += 0.001
      if keys_pressed[pygame.K_RIGHT]:
        self.aceleracao_angular_lateral -= 0.001
      if self.aceleracao_angular_lateral > 0.3:
        self.aceleracao_angular_lateral = 0.3
      self.angulo += self.aceleracao_angular_lateral
    else:
      self.aceleracao_angular_lateral = 0
    if keys_pressed[pygame.K_UP]:
      self.forca_propulsao += 500
      #som_aceleracao_propulsor.play()
      self.fumaca.add(self.x, self.y + 25)
      if(self.forca_propulsao > self.gravidade * self.massa * 3):
        self.forca_propulsao = self.gravidade * self.massa * 3
      self.forca_propulsao_x = self.forca_propulsao * math.cos(angulo_radianos)
      self.forca_propulsao_y = self.forca_propulsao * math.sin(angulo_radianos)
    else:
      self.forca_propulsao = 0
      self.forca_propulsao_x = 0
      self.forca_propulsao_y = 0

    
    self.forca_propulsao_y -= self.massa * self.gravidade #gravidade
    
    self.aceleracao_propulsao_x = self.forca_propulsao_x / self.massa
    self.aceleracao_propulsao_y = self.forca_propulsao_y / self.massa
    
    self.velocidade_x = self.velocidade_x_inicial + self.aceleracao_propulsao_x * self.tempo
    self.velocidade_y = self.velocidade_y_inicial + self.aceleracao_propulsao_y * self.tempo
    
    self.posicao_x = self.posicao_inicial_x + self.velocidade_x_inicial * self.tempo + 0.5 * self.aceleracao_propulsao_x * math.pow(self.tempo, 2)
    self.posicao_y = self.posicao_inicial_y + self.velocidade_y_inicial * self.tempo + 0.5 * self.aceleracao_propulsao_y * math.pow(self.tempo, 2)
    
    self.velocidade_x_inicial = self.velocidade_x
    self.velocidade_y_inicial = self.velocidade_y
    self.posicao_inicial_x = self.posicao_x
    self.posicao_inicial_y = self.posicao_y
    
    self.x += self.velocidade_x + 0.1*random.random()*random.choice([-1, 1])
    self.y -= self.velocidade_y
    
    self.angulo += 0.3*random.random()*random.choice([-1, 1])
    self.angulo_direcao = math.degrees(math.atan2(self.velocidade_y, self.velocidade_x)) - 45
    angulo_diferenca = (self.angulo_direcao - self.angulo + 180) % 360 - 180
    ajuste_angular = 0.005 * angulo_diferenca
    self.angulo += ajuste_angular

    if self.y > screen_height:
      self.y = screen_height
      self.velocidade_y_inicial = 0
      self.velocidade_x_inicial = 0
      self.velocidade_x = 0
      self.angulo = 45 + 0.01*random.random()*random.choice([-1, 1])
    self.fumaca.update()
  
  def draw(self, camera_offset_x, camera_offset_y):
    self.camera_offset_x = camera_offset_x
    self.camera_offset_y = camera_offset_y
    foguete_rotacionado = pygame.transform.rotate(self.img, self.angulo)
    rect = foguete_rotacionado.get_rect(center=(self.x - camera_offset_x, self.y - camera_offset_y))
    screen.blit(foguete_rotacionado, rect.topleft)
    self.fumaca.draw(-camera_offset_x, - camera_offset_y)



