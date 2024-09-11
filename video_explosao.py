import pygame
import os

pygame.init()

largura_tela, altura_tela = 1080, 720
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Sequência de Imagens")

def carregar_imagens(pasta):
    imagens = []
    for nome_arquivo in sorted(os.listdir(pasta)):
        if nome_arquivo.endswith('.png'):
            caminho = os.path.join(pasta, nome_arquivo)
            imagem = pygame.image.load(caminho).convert_alpha()
            imagens.append(imagem)
    return imagens

pasta_imagens = "explosao_frames"
imagens = carregar_imagens(pasta_imagens)

fps = 30
clock = pygame.time.Clock()
indice_imagem = 0
cor = (0, 0, 255)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    tela.fill(cor)
    tela.blit(imagens[indice_imagem], (0, 0))
    pygame.display.flip()

    indice_imagem += 1
    if indice_imagem >= len(imagens):
        indice_imagem = 0

    clock.tick(fps)

pygame.quit()
