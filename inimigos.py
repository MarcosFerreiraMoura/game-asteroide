
import pygame
import random



class Inimigos(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image  = pygame.image.load("dados\planetas\PinkPlanet.png")
        self.image = pygame.transform.scale(self.image, (100,100)) 
        self.rect = pygame.Rect(50, 50, 80, 80)

        self.rect.x = 1000 + random.randint(1,500)
        self.rect.y =random.randint(1, 400)

        self.speed =  1+ random.random()*2

    def update(self, *args):

        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill