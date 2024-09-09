import random
import pygame
from foguete import Foguete
from inimigos import Inimigos
from gameOver import GameOver
import boss
from boss import naveBoss
import subprocess

pygame.init()

# tela do jogo
info = pygame.display.Info()
largura = info.current_w
altura = info.current_h
tela  =  pygame.display.set_mode((largura, altura))

#plano de fundo
background = pygame.image.load('assets/background/Space-Background-4.jpg').convert()
img = pygame.transform.scale(background, (largura, altura))
pygame.display.set_caption("Batalha no Espaço")

#musicas 
pygame.mixer.music.load("assets/background/Space Atmosphere.mp3")
pygame.mixer.music.play(-1)

#groups
objectGroup1 = pygame.sprite.Group() #nivel 1
objectGroup2 = pygame.sprite.Group() #nivel 2
inimigoGroup = pygame.sprite.Group()
gameOverGroup = pygame.sprite.Group()

#objetos sem groups
newPlayer = Foguete(objectGroup1, objectGroup2)
gameOver = GameOver(gameOverGroup)

newBoss = None
isGameOver = False
loop = True
clock  =  pygame.time.Clock()
x = 0
timer = 0
isPause = False

def reiniciarGame():
    global newPlayer, timer, isGameOver
    objectGroup1.empty()
    objectGroup2.empty()
    inimigoGroup.empty()
    boss.tiroGroupBoss.empty()
    newPlayer = Foguete(objectGroup1, objectGroup2)
    timer = 0
    isGameOver = False
    pygame.mixer.music.play(-1)
    newPlayer.alive = True

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
                    subprocess.Popen(["D:/Usuarios/fabio/Área de Trabalho/github/fabioqueiroz1415/uni/computacaografica/game-asteroide/.venv/Scripts/python.exe", "menu_iniciar.py"])
                elif gameOver.botaoTentarNovamente.rect.collidepoint(mouse):
                    reiniciarGame()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                isPause = not isPause
                if isPause:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
    
    if not isGameOver and not isPause and newPlayer.alive:
        objectGroup1.update()
        objectGroup2.update(eventos)
        
        if not timer % 60:
            timer = 0
            if random.random() < 0.4:
                novoInimigo = Inimigos(objectGroup2, inimigoGroup)
            if random.random() < 0.01:
                if not (newBoss and newBoss.alive()):
                    newBoss = naveBoss(objectGroup2, inimigoGroup)
        timer += 1
        if pygame.sprite.spritecollide(newPlayer, inimigoGroup, False, pygame.sprite.collide_mask) or not newPlayer.alive:
            pygame.mixer.music.stop()
            isGameOver = True

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
    elif isGameOver or not newPlayer.alive:
        objectGroup2.add(gameOverGroup)
    
    objectGroup1.draw(tela)
    objectGroup2.draw(tela)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)