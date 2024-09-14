import pygame
import os
import random

def escala(img: pygame.Surface, fator):
  w, h = img.get_width() * fator, img.get_height() * fator
  return pygame.transform.scale(img, (int(w), int(h)))

class ExplosaoSprite(pygame.sprite.Sprite):
    def __init__(self, fps=30):
        super().__init__()
        self.imagens = []
        self.fps = fps
        self.tempo_entre_frames = 1000 // fps
        self.indice_imagem = -1
        self.tempo_ultimo_frame = pygame.time.get_ticks()
        self.rodando = True
        pasta = f"assets/explosao_frames/{random.randint(0, 3)}" #alterado por fábio

        for arquivo in sorted(os.listdir(pasta)):
            if arquivo.endswith(".png"):
                try:
                    imagem = pygame.image.load(os.path.join(pasta, arquivo)).convert_alpha()
                    imagem = escala(imagem, 0.13) #inserido por fábio
                    self.imagens.append(imagem)
                except pygame.error as e:
                    print(f"Não foi possível carregar a imagem {arquivo}: {e}")

        if not self.imagens:
            print("Nenhuma imagem carregada. Verifique o caminho e o formato das imagens.")

        self.posicao = (0, 0)
        self.image = self.imagens[self.indice_imagem]
        self.rect = self.image.get_rect(center=self.posicao) #alterado por fábio

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_frame >= self.tempo_entre_frames:
            self.indice_imagem += 1
            self.tempo_ultimo_frame = agora
            if self.indice_imagem >= len(self.imagens):
                self.rodando = False
                self.kill()  # Remove o sprite do grupo quando a animação termina
            else:
                self.image = self.imagens[self.indice_imagem]
                self.rect = self.image.get_rect(center=self.posicao) #alterado por fabio

############   para teste   ############
if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 1080, 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    grupo_explosao = pygame.sprite.Group()
    explosao = ExplosaoSprite()
    explosao.posicao = (screen_width//2, screen_height//2)
    grupo_explosao.add(explosao)

    while grupo_explosao:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                grupo_explosao.empty()

        grupo_explosao.update()
        screen.fill((0, 0, 0))
        grupo_explosao.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

############   para teste   ############
