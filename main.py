import random
import pygame
from foguete import Foguete
from inimigos import Inimigos
from fogo import Fogo

pygame.init()

# tela do jogo
largura = 1000
altura = 600
tela  =  pygame.display.set_mode((largura, altura))

#definindo fundo
background = pygame.image.load('dados/imagens/background/Space-Background-4.jpg').convert()
img = pygame.transform.scale(background, (largura, altura))
pygame.display.set_caption("Batalha no Espaço")

#musicas 
pygame.mixer.music.load("dados/audios/Space Atmosphere.mp3")
pygame.mixer.music.play(-1)

objectGroup1 = pygame.sprite.Group() #nivel 1
objectGroup2 = pygame.sprite.Group() #nivel 2
inimigoGroup = pygame.sprite.Group()

newPlayer = Foguete(objectGroup1, objectGroup2)

timer = 0
gameover = False
loop = True
clock  =  pygame.time.Clock()
x = 0
while loop:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit() 
            loop = False
    
    if not gameover:
        objectGroup1.update()
        objectGroup2.update()
        
        if not timer % 60:
            timer = 0
            if random.random() < 0.4:
                novoInimigo = Inimigos(objectGroup2, inimigoGroup)
        colisao = pygame.sprite.spritecollide(newPlayer, inimigoGroup, False, pygame.sprite.collide_mask)
        timer += 1
        
    if colisao:
        pygame.mixer.music.stop()
        gameover = True
    
    #draw
    tela.fill("black")
    
    if -x >= largura:
        x += largura
    x -= 0.25
    for i in range(2):
        if i % 2:
            img_atualizada = pygame.transform.flip(img, True, False)
        else:
            img_atualizada = img
        tela.blit(img_atualizada,(x + largura * i, 0))
    objectGroup1.draw(tela)
    objectGroup2.draw(tela)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)