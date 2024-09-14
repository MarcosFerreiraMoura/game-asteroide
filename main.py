import random
import pygame
import foguete
from inimigos import Inimigos
from gameOver import GameOver
import boss
from boss import naveBoss
import subprocess
from explosao_video import ExplosaoSprite
import copy

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
explosaoGroup = pygame.sprite.Group()
inimigoGroup = pygame.sprite.Group()
gameOverGroup = pygame.sprite.Group()

explosaoObject = ExplosaoSprite()

#objetos sem groups
newPlayer = foguete.Foguete(objectGroup1, objectGroup2)
gameOver = GameOver(gameOverGroup)

#efeitos sonoros
explosao = pygame.mixer.Sound("assets/fogos/explosaoSOM.mp3")



newBoss = None
isGameOver = False
loop = True
clock  =  pygame.time.Clock()
explosao_time = None
x = 0
timer = 0
isPause = False

def reiniciarGame():
    global newPlayer, timer, isGameOver
    objectGroup1.empty()
    objectGroup2.empty()
    inimigoGroup.empty()
    explosaoGroup.empty()
    boss.tiroGroupBoss.empty()
    newPlayer = foguete.Foguete(objectGroup1, objectGroup2)
    timer = 0
    isGameOver = False
    pygame.mixer.music.play(-1)

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
    
    if (not isGameOver) and (not isPause) and newPlayer.alive():
        objectGroup1.update()
        objectGroup2.update(eventos)
        
        if not timer % 60:
            timer = 0
            if random.random() < 0.4:
                novoInimigo = Inimigos(objectGroup2, inimigoGroup)
            if random.random() < 0.1:
                if not (newBoss and newBoss.alive()):
                    newBoss = naveBoss(objectGroup2, inimigoGroup)
        timer += 1
        
        hits = pygame.sprite.groupcollide(foguete.tiroGroup, inimigoGroup, True, True, pygame.sprite.collide_mask)
        if hits:
            for hit in hits:
                explosao.play()
                explosao_time = pygame.time.get_ticks()
                
                # cópia da classe já instanciada
                video_explosao = copy.copy(explosaoObject)
                video_explosao.posicao = hit.rect.center
                explosaoGroup.add(video_explosao)
                
        if pygame.sprite.spritecollide(newPlayer, inimigoGroup, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(newPlayer, boss.tiroGroupBoss, False, pygame.sprite.collide_mask):
            explosao.play()
            explosao_time = pygame.time.get_ticks()
            
            # cópia da classe já instanciada
            video_explosao = copy.copy(explosaoObject)
            video_explosao.posicao = newPlayer.rect.center
            explosaoGroup.add(video_explosao)
            newPlayer.kill()
            pygame.mixer.music.stop()
            
            isGameOver = True

        if -x >= largura:
            x += largura
        x -= 0.25
        for i in range(2):
            if i % 2:
                img_atualizada = pygame.transform.flip(img, True, False)
            else:
                img_atualizada = img
            tela.blit(img_atualizada,(x + largura * i, 0))
    elif isGameOver or not newPlayer.alive():
        # Checa o tempo para mostrar a tela de Game Over
        if explosao_time and pygame.time.get_ticks() - explosao_time >= 2000:
            objectGroup2.add(gameOverGroup)
    
    # Mantém a animação da explosão ativa mesmo no Game Over
    explosaoGroup.update()
    
    objectGroup1.draw(tela)
    explosaoGroup.draw(tela)
    objectGroup2.draw(tela)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)