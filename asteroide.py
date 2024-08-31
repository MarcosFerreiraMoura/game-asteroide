import random
import pygame
from foguete import Foguete
from inimigos import Inimigos
from tiro import Tiro
from fumaca import FumacaWhite


pygame.init()

# tela do jogo
largura = 1000
altura = 600
tela  =  pygame.display.set_mode((largura, altura))

#definindo fundo
background = pygame.image.load('dados/background\Space-Background-4.jpg').convert()
img = pygame.transform.scale(background, (largura, altura))
pygame.display.set_caption("Batalha no Espaço")

#musicas 
pygame.mixer.music.load("dados\Space Atmosphere.mp3")
pygame.mixer.music.play(-1)

#efeitos sonoros
tiro = pygame.mixer.Sound("dados\plane_imagem\Fire 1.mp3")

objectGroup = pygame.sprite.Group()
inimigoGroup = pygame.sprite.Group()
tiroGroup = pygame.sprite.Group()


player = Foguete(objectGroup)
fumacaGroup = pygame.sprite.Group()

timer = 0
gameover = False
loop = True
clock  =  pygame.time.Clock()
while loop:
         
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit() 
                loop = True              
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not gameover:
                    tiro.play()
                    newTiro = Tiro(objectGroup, tiroGroup )
                    newTiro.rect.center = player.rect.center 
       
        if not gameover:
           
            objectGroup.update()
            # fumacaGroup.update()
            timer += 1
            if timer > 60:
                timer = 0
                if random.random() < 0.4:
                    novoInimigo = Inimigos(objectGroup, inimigoGroup)
            colisao = pygame.sprite.spritecollide(player, inimigoGroup, False, pygame.sprite.collide_mask)
            
            
        if colisao:
            pygame.mixer.music.stop()
            gameover = True

        hits  = pygame.sprite.groupcollide(tiroGroup, inimigoGroup, True, True, pygame.sprite.collide_mask)
        if hits:
            for hit in hits:
                for i in range(1):
                  FumacaWhite(hit.rect.center, [objectGroup, fumacaGroup])  
        
        #draw
        tela.fill("black") 
        tela.blit(img,(0, 0))       
        objectGroup.draw(tela)
        fumacaGroup.draw(tela)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)