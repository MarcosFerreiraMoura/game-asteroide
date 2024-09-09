import random
import pygame
import time
from explosão import ExplosaoParticulas
from foguete import Foguete
from inimigos import Inimigos
from gameOver import GameOver

pygame.init()

# tela do jogo
info = pygame.display.Info()
largura = info.current_w
altura = info.current_h


tela = pygame.display.set_mode((largura, altura))

# plano de fundo
background = pygame.image.load('game-asteroide/assets/background/Space-Background-4.jpg').convert()
img = pygame.transform.scale(background, (largura, altura))
pygame.display.set_caption("Batalha no Espaço")

# músicas 
pygame.mixer.music.load("game-asteroide/assets/background/Space Atmosphere.mp3")
pygame.mixer.music.play(-1)

# efeitos sonoros
explosao = pygame.mixer.Sound("game-asteroide/assets/fogos/explosaoSOM.mp3")

# grupos
objectGroup1 = pygame.sprite.Group() # nível 1
objectGroup2 = pygame.sprite.Group() # nível 2
inimigoGroup = pygame.sprite.Group()
gameOverGroup = pygame.sprite.Group()

# objetos sem grupos
newPlayer = Foguete(objectGroup1, objectGroup2)
gameOver = GameOver(gameOverGroup)

timer = 0
isGameOver = False
explosao_time = None  # Inicializando explosao_time
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
                    # adicionar tela de início depois
                elif gameOver.botaoTentarNovamente.rect.collidepoint(mouse):
                    reiniciarGame()

    # Atualizações principais do jogo
    if not isGameOver:
        objectGroup1.update()
        objectGroup2.update(eventos)
        
        # Atualiza o timer e cria novos inimigos
        if not timer % 60:
            timer = 0
            if random.random() < 0.4:
                novoInimigo = Inimigos(objectGroup2, inimigoGroup)
        timer += 1

        # Checa colisão entre jogador e inimigos
        if pygame.sprite.spritecollide(newPlayer, inimigoGroup, False, pygame.sprite.collide_mask):
            explosao.play()
            explosao_time = pygame.time.get_ticks()
            # Criar partículas de explosão
            for i in range(8):
                explosao_particulas = ExplosaoParticulas(newPlayer.rect.center, objectGroup2)
            
            newPlayer.kill()
            pygame.mixer.music.stop()

            # Inicializa explosao_time com o tempo atual
            isGameOver = True

    else:
        # Mantém a animação da explosão ativa mesmo no Game Over
        for particula in objectGroup2:
            if isinstance(particula, ExplosaoParticulas):
                particula.update()

        # Checa o tempo para mostrar a tela de Game Over
        if explosao_time and pygame.time.get_ticks() - explosao_time >= 2000:
            objectGroup2.add(gameOverGroup)

    # Desenho na tela
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
