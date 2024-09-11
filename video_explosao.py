import pygame
import os

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura_tela, altura_tela = 1080, 720
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Sequência de Imagens")

# Carrega todas as imagens da sequência
def carregar_imagens(pasta):
    imagens = []
    for nome_arquivo in sorted(os.listdir(pasta)):
        if nome_arquivo.endswith('.png'):
            caminho = os.path.join(pasta, nome_arquivo)
            imagem = pygame.image.load(caminho).convert_alpha()
            imagens.append(imagem)
    return imagens

# Caminho da pasta com imagens
pasta_imagens = "C:/Users/pires/OneDrive/Área de Trabalho/trabalhodogordão/explosao_frames"
imagens = carregar_imagens(pasta_imagens)

# Configurações do vídeo
fps = 30
clock = pygame.time.Clock()
indice_imagem = 0

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    # Atualiza o frame da imagem
    tela.fill((0, 0, 0))  # Limpa a tela com cor preta
    tela.blit(imagens[indice_imagem], (0, 0))
    pygame.display.flip()

    # Avança para o próximo frame
    indice_imagem += 1
    if indice_imagem >= len(imagens):
        indice_imagem = 0  # Volta ao início

    clock.tick(fps)  # Controla a taxa de quadros

# Encerra o Pygame
pygame.quit()
