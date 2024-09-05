import pygame


# Limpar o módulo cache se necessário

class TiroEspecial(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("dados/tiroAzul.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.speed = 6
        self.explodiu = False

    def update(self, *args):
        self.rect.x += self.speed

    def explodir(self):
        if not self.explodiu:
            self.explodiu = True
            tiros_menores = []
            for i in range(-2, 360):
                tiro_menor = TiroMenor(self.rect.centerx, self.rect.centery, i, self.groups())
                tiros_menores.append(tiro_menor)
            self.kill()
            return tiros_menores

class TiroMenor(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load("dados/tiroAzul.png")  
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = direction * 3
        self.speed_y = 3 

    def update(self, *args):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y

        if self.rect.left > 1000 or self.rect.bottom < 0:
            self.kill()