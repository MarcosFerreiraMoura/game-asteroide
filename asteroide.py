import random
import pygame
from foguete import Foguete
from inimigos import Inimigos
from tiro import Tiro
from fumaca import FumacaWhite
from tiro_especial import TiroEspecial

pygame.init()

# Tela do jogo
#info = pygame.display.Info()
largura = 1000
altura = 600
tela = pygame.display.set_mode((largura, altura))

# Definindo fundo
background = pygame.image.load('dados\/background\Space-Background-4.jpg').convert()
img = pygame.transform.scale(background, (largura, altura))
pygame.display.set_caption("Batalha no Espaço")

# Músicas 
pygame.mixer.music.load("dados\planetas\Space Atmosphere.mp3")
pygame.mixer.music.play(-1)

# Efeitos sonoros
tiro_sound = pygame.mixer.Sound("dados\plane_imagem\Fire 1.mp3")
tiro_especial_sound = pygame.mixer.Sound("dados\plane_imagem\Fire 5.mp3")
tiro_menor_sound = pygame.mixer.Sound("dados\plane_imagem\Fire 3.mp3")


objectGroup = pygame.sprite.Group()
inimigoGroup = pygame.sprite.Group()
tiroGroup = pygame.sprite.Group()
fumacaGroup = pygame.sprite.Group()

player = Foguete(objectGroup)

# Variáveis para controle do tiro especial
tiro_especial = None

timer = 0
gameover = False
loop = True
clock = pygame.time.Clock()
x = 0

while loop:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            loop = True
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not gameover:
                tiro_sound.play()
                newTiro = Tiro(objectGroup, tiroGroup)
                newTiro.rect.midleft = player.rect.midright
            elif evento.key == pygame.K_p and not gameover:
                if tiro_especial:  # Se já existe um tiro especial, faz ele explodir
                    tiro_menor_sound.play()
                    tiros_menores = tiro_especial.explodir()
                    if tiros_menores:
                        objectGroup.add(*tiros_menores)
                        tiroGroup.add(*tiros_menores)
                        tiro_especial.kill()  # Remove o tiro especial após explodir
                        tiro_especial = None
                else:  # Se não há um tiro especial ativo, cria um novo
                    tiro_especial_sound.play()
                    tiro_especial = TiroEspecial(objectGroup, tiroGroup)
                    tiro_especial.rect.midleft = player.rect.midright

    if not gameover:
        objectGroup.update()

        if not timer % 60:
            timer = 0
            if random.random() < 0.45:
                novoInimigo = Inimigos(objectGroup, inimigoGroup)
        colisao = pygame.sprite.spritecollide(player, inimigoGroup, False, pygame.sprite.collide_mask)
        timer += 1

        # Verifica colisão entre tiro especial e inimigos
        if tiro_especial:
            hits_especial = pygame.sprite.spritecollide(tiro_especial, inimigoGroup, True, pygame.sprite.collide_mask)
            if hits_especial:
                tiro_especial.kill()
                tiro_especial = None  # Certifica-se de que o tiro especial não existe mais

    if colisao:
        pygame.mixer.music.stop()
        gameover = True

    hits = pygame.sprite.groupcollide(tiroGroup, inimigoGroup, True, True, pygame.sprite.collide_mask)
    if hits:
        for hit in hits:
            for i in range(1):
                FumacaWhite(hit.rect.center, [objectGroup, fumacaGroup])

    # Draw
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
    objectGroup.draw(tela)
    fumacaGroup.draw(tela)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)