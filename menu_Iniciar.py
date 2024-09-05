# menu.py
import pygame
import subprocess
import sys

# Inicializar o Pygame
pygame.init()
pygame.mixer.music.load("dados/background/StockTune-Stellar Symphony.mp3")  # Carrega o arquivo de som
pygame.mixer.music.play(-1) 

# Configurações da tela
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tela Inicial")

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Carregar imagem de fundo
background = pygame.image.load("dados/background/Menu_game.PNG")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Classe Button
class Button:
    def __init__(self, text, rect, color, hover_color, font):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.color = color
        self.hover_color = hover_color
        self.font = font

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, white)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

# Classe para a Tela Inicial
class InitialScreen:
    def __init__(self):
        self.button = Button("Iniciar", [screen_width // 2 - 100, screen_height // 2 - 50, 200, 100], black, red, pygame.font.Font(None, 74))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.is_clicked():
                        print("Iniciar o jogo")
                        pygame.quit()  # Encerra a tela inicial
                        self.start_game()  # Inicia o jogo principal

            # Desenhar o fundo
            screen.blit(background, (0, 0))

            # Desenhar o botão "Iniciar"
            self.button.draw(screen)

            # Atualizar a tela
            pygame.display.flip()

    def start_game(self):
        # Usar subprocess para iniciar o jogo principal
        subprocess.Popen(["python", "main.py"])

# Inicializar e rodar a tela inicial
if __name__ == "__main__":
    initial_screen = InitialScreen()
    initial_screen.run()
