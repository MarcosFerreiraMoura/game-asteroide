
import pygame

from pygame.locals import*



class Tiro(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image  = pygame.image.load("dados/tiroRoxo.png")
        self.image = pygame.transform.scale(self.image, (10,10)) 
        self.rect = self.image.get_rect()
        
        self.speed = 4

    def update(self, *args):

        self.rect.x += self.speed

        if self.rect.left > 1000:
            self.kill
    
    