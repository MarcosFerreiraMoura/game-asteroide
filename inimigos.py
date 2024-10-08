
import pygame
import random
from fumaca import FumacaWhite
import foguete

fumacaGroup = pygame.sprite.Group()

info = pygame.display.Info()

class Inimigos(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.objectGroup = groups[0]
        self.inimigoGroup = groups[1]

        self.image  = pygame.image.load("dados/imagens/planetas/PinkPlanet.png")
        self.image = pygame.transform.scale(self.image, (100,100)) 
        self.rect = pygame.Rect(50, 50, 80, 80)

        self.rect.x = info.current_w + random.randint(1,500)
        self.rect.y = random.randint(1, info.current_h - 200)

        self.speed =  1+ random.random()*2

    def update(self):

        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()
        
        hits  = pygame.sprite.groupcollide(foguete.tiroGroup, self.inimigoGroup, True, True, pygame.sprite.collide_mask)
        if hits:
            for hit in hits:
                for i in range(1):
                    newFumaca = FumacaWhite(hit.rect.center, self.objectGroup, fumacaGroup)