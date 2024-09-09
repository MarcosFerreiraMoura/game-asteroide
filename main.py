import random
import pygame
from foguete import Foguete
from inimigos import Inimigos
from gameOver import GameOver

pygame.init()

# tela do jogo
info = pygame.display.Info()
largura = info.current_w
altura = info.current_h
largura = 1000
altura = 600

tela  =  pygame.display.set_mode((largura, altura))

# plano de fundo
background = pygame.image.load('assets/background/Space-Background-4.jpg').convert()
img = pygame.transform.scale(background, (largura, altura))
pygame.display.set_caption("Batalha no Espaço")

# musicas 
pygame.mixer.music.load("assets/background/Space Atmosphere.mp3")
pygame.mixer.music.play(-1)

# grupos de sprites
objectGroup1 = pygame.sprite.Group()  # Nível 1
objectGroup2 = pygame.sprite.Group()  # Nível 2
inimigoGroup = pygame.sprite.Group()
gameOverGroup = pygame.sprite.Group()

# objetos sem groups
newPlayer = Foguete(objectGroup1, objectGroup2)
gameOver = GameOver(gameOverGroup)

timer = 0
isGameOver = False
loop = True
clock = pygame.time.Clock()
x = 0

def reiniciarGame():
    global newPlayer, timer, isGameOver
    objectGroup1.empty()
    objectGroup2.empty()
    inimigoGroup.empty()
    newPlayer = Foguete(objectGroup1, objectGroup2)
    timer = 0
    isGameOver = False
    pygame.mixer.music.play(-1)

def update_sprites_with_events(group, eventos):
    for sprite in group:
        if hasattr(sprite, 'update'):  # verifica se o sprite tem o metodo update
            # Tenta passar eventos se o método aceitar
            try:
                sprite.update(eventos)
            except TypeError:
                sprite.update()  # se nao aceitar chama update sem argumentos

while loop:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            loop = False
        if evento.type == pygame.MOUSEBUTTONDOWN and isGameOver:
            if evento.button == 1:
                mouse = pygame.mouse.get_pos()
                if gameOver.botaoMenu.rect.collidepoint(mouse):
                    loop = False
                  
                elif gameOver.botaoTentarNovamente.rect.collidepoint(mouse):
                    reiniciarGame()

    if not isGameOver:
        objectGroup1.update()
        update_sprites_with_events(objectGroup2, eventos)  # chama a funcao que lida com eventos nas sprites
        
        if not timer % 60:
            timer = 0
            if random.random() < 0.4:
                novoInimigo = Inimigos(objectGroup2, inimigoGroup)
        timer += 1
        
        if pygame.sprite.spritecollide(newPlayer, inimigoGroup, False, pygame.sprite.collide_mask):
            pygame.mixer.music.stop()
            isGameOver = True
    else:
        objectGroup2.add(gameOverGroup)

    tela.fill("black")

    if -x >= largura:
        x += largura
    x -= 0.25
    
    for i in range(2):
        if i % 2:
            img_atualizada = pygame.transform.flip(img, True, False)
        else:
            img_atualizada = img
        tela.blit(img_atualizada, (x + largura * i, 0))

    objectGroup1.draw(tela)
    objectGroup2.draw(tela)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
