import pygame
import random
import math
import os

def escala(img: pygame.Surface, fator):
    w, h = img.get_width() * fator, img.get_height() * fator
    return pygame.transform.scale(img, (int(w), int(h)))

class ExplosaoParticulas(pygame.sprite.Sprite):
    def __init__(self, posicao, *groups):
        super().__init__(*groups)
        
        # Carrega a imagem da partícula
        self.image_original = random.choice([
            pygame.image.load('assets/fogos/explosaofullHD.png').convert_alpha(),
            pygame.image.load('assets/fogos/explosaofullHD2.png').convert_alpha(),
        ])
        self.image_original = escala(self.image_original, random.uniform(0.7, 0.9))  # Reduz e randomiza o tamanho da partícula
        self.image = self.image_original.copy()  # Cópia da imagem para manipular
        
        self.rect = self.image.get_rect(center=posicao)

        # Define as propriedades da partícula
        self.alpha = 200  # Transparência da partícula
        self.velocidade = random.uniform(1, 1.5)  # Velocidade da partícula
        self.angulo = random.uniform(0, 2 * math.pi)  # Ângulo aleatório (em radianos)

        # Calcula as velocidades x e y com base no ângulo
        self.velocidade_x = self.velocidade * math.cos(self.angulo)
        self.velocidade_y = self.velocidade * math.sin(self.angulo)

        # Define um tempo de vida ajustado para que as partículas durem o tempo necessário
        self.tempo_de_vida = random.randint(90, 120)  # Ajuste o intervalo de acordo com a necessidade

    def update(self):
        # Atualiza a posição da partícula
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        
        # Desacelera a partícula ao longo do tempo
        self.velocidade_x *= 0.98
        self.velocidade_y *= 0.98

        # Diminui gradualmente a opacidade (fade out)
        self.alpha -= 2  # Reduz mais rapidamente para desaparecer em tempo razoável
        self.image = self.image_original.copy()  # Restaura a imagem original para aplicar o alfa
        self.image.set_alpha(self.alpha)

        # Diminui o tempo de vida da partícula
        self.tempo_de_vida -= 1

        # Remove a partícula quando ela "morre"
        if self.alpha <= 0 or self.tempo_de_vida <= 0:
            self.kill()

# Função para salvar os frames da explosão
def salvar_frames(screen, grupo_explosao: pygame.sprite.Group, numero_frames=90, diretorio="1"):
    diretorio = f"assets/explosao_frames/{diretorio}"
    pygame.display.set_caption(f"salvando em {diretorio}")
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)  # Cria o diretório para os frames se não existir

    frame_num = 0
    clock = pygame.time.Clock()
    
    # Criar uma superfície transparente para salvar os frames
    surface_transparente = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    
    while len(grupo_explosao) < 50:
        ExplosaoParticulas((screen_width//2, screen_height//2), grupo_explosao)

    while frame_num < numero_frames:
        surface_transparente.fill((0, 0, 0, 0))

        grupo_explosao.update()
        grupo_explosao.draw(surface_transparente)
        grupo_explosao.draw(screen) #inserido por fábio

        nome_arquivo = f"{diretorio}/frame_{frame_num:03d}.png"
        
        pygame.image.save(surface_transparente, nome_arquivo)
        pygame.display.set_caption(f"salvando em {nome_arquivo}... {frame_num}/{numero_frames}")
        frame_num += 1

        pygame.display.flip()

        if frame_num >= len(grupo_explosao) and len(grupo_explosao) > 0:
            surface_transparente.fill((0, 0, 0, 0))
            pygame.image.save(surface_transparente, nome_arquivo)
            pygame.display.set_caption(f"salvando em {nome_arquivo}... {frame_num}/{numero_frames}")

        clock.tick(30)

######## para teste ########
if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 1080, 720
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)

    grupo_explosao = pygame.sprite.Group()
    for _ in range(50):
        ExplosaoParticulas((screen_width//2, screen_height//2), grupo_explosao)

    salvar_frames(screen, grupo_explosao, diretorio="0")

    pygame.quit()
    
######## para teste ########
