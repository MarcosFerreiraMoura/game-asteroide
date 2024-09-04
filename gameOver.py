import pygame
pygame.init()

info = pygame.display.Info()
largura = info.current_w
altura = info.current_h

def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))

class GameOver():
  def __init__(self, *groups):
    self.imagemGameOver = imagemGameOver(*groups)
    self.botaoTentarNovamente = botaoTentarNovamente(*groups)
    self.botaoMenu = botaoMenu(*groups)

class imagemGameOver(pygame.sprite.Sprite):
  def __init__(self, *groups):
    super().__init__(*groups)
    self.image = pygame.image.load('dados/imagens/gameOver/gameOver.png').convert_alpha()
    self.rect = self.image.get_rect(center = (largura//2, altura//2 - 100))

class botaoTentarNovamente(pygame.sprite.Sprite):
  def __init__(self, *groups):
    super().__init__(*groups)
    self.image = pygame.image.load('dados/imagens/gameOver/tentarNovamente.png').convert_alpha()
    self.image = escala(self.image, 0.1)
    self.rect = self.image.get_rect(center = (largura//2 - 200, altura//2 + 150))

class botaoMenu(pygame.sprite.Sprite):
  def __init__(self, *groups):
    super().__init__(*groups)
    self.image = pygame.image.load('dados/imagens/gameOver/menu.png').convert_alpha()
    self.image = escala(self.image, 0.1)
    self.rect = self.image.get_rect(center = (largura//2 + 200, altura//2 + 150))