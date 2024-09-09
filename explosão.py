import pygame
import random
import math

def escala(img: pygame.Surface, fator):
    w, h = img.get_width() * fator, img.get_height() * fator
    return pygame.transform.scale(img, (int(w), int(h)))

class ExplosaoParticulas(pygame.sprite.Sprite):
    def __init__(self, posicao, *groups):
        super().__init__(*groups)
        
        # Carrega a imagem da partícula
        self.image_original = random.choice([
            pygame.image.load('assets/fogos/explosao0.png').convert_alpha(),
            pygame.image.load('assets/fogos/explosao.png').convert_alpha()
        ])
        self.image_original = escala(self.image_original, random.uniform(3, 3.1))  # Reduz e randomiza o tamanho da partícula
        self.image = self.image_original.copy()  # Cópia da imagem para manipular
        
        self.rect = self.image.get_rect(center=posicao)

        # Define as propriedades da partícula
        self.alpha = 200  # Transparência da partícula
        self.velocidade = random.uniform(1, 1.5)  # Velocidade da partícula
        self.angulo = random.uniform(0, 2 * math.pi)  # Ângulo aleatório (em radianos)

        # Calcula as velocidades x e y com base no ângulo
        self.velocidade_x = self.velocidade * math.cos(self.angulo)
        self.velocidade_y = self.velocidade * math.sin(self.angulo)

        # Vida útil e escala de cada partícula
        self.tempo_de_vida = random.randint(60, 80)  # Duração da partícula

    def update(self):
        # Atualiza a posição da partícula
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y
        
        # Desacelera a partícula ao longo do tempo
        self.velocidade_x *= 0.98
        self.velocidade_y *= 0.98

        # Diminui gradualmente a opacidade (fade out)
        self.alpha -= 4  # Reduz mais rapidamente para desaparecer em tempo razoável
        self.image = self.image_original.copy()  # Restaura a imagem original para aplicar o alfa
        self.image.set_alpha(self.alpha)

        # Diminui o tempo de vida da partícula
        self.tempo_de_vida -= 1

        # Remove a partícula quando ela "morre"
        if self.alpha <= 0 or self.tempo_de_vida <= 0:
            self.kill()



