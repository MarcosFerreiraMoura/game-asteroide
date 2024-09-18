
import pygame
import random
from fumaca import FumacaWhite
import foguete

fumacaGroup = pygame.sprite.Group()

info = pygame.display.Info()

def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))

class Inimigos(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.objectGroup2 = groups[0]
        self.inimigoGroup = groups[1]
    
        # aqui escolhe de forma aleatoria um invasor de 0 a 9
        self.idInvasor = random.randint(0, 9)

        # Cacarrega a imagem do invasor 
        self.image  = pygame.image.load(f"assets/invasores/invasor-{self.idInvasor}.png").convert_alpha()
        self.image = escala(self.image, 0.17)

        self.rect = pygame.Rect(50, 50, 80, 80)

        self.rect.x = info.current_w + random.randint(1,500)
        self.rect.y = random.randint(1, info.current_h - 200)

        self.speed =  1 + random.random() * 2

    def update(self, *args):

        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()
                    