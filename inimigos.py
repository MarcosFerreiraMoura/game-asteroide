
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
        self.objectGroup = groups[0]
        self.inimigoGroup = groups[1]
    
        self.idPlaneta = random.randint(0, 9)
        self.image  = pygame.image.load(f"game-asteroide/assets/planetas/planet-{self.idPlaneta}.png").convert_alpha()
        self.image = escala(self.image, 0.07)
        self.rect = pygame.Rect(50, 50, 80, 80)

        self.rect.x = info.current_w + random.randint(1,500)
        self.rect.y = random.randint(1, info.current_h - 200)

        self.speed =  1+ random.random()*2

    def update(self, *args):

        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()
        
        hits  = pygame.sprite.groupcollide(foguete.tiroGroup, self.inimigoGroup, True, True, pygame.sprite.collide_mask)
        if hits:
            for hit in hits:
                for i in range(1):
                    newFumaca = FumacaWhite(hit.rect.center, self.objectGroup, fumacaGroup)