import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen_info = pygame.display.Info()
SCREEN_WIDTH = 938
SCREEN_HEIGHT = 528
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Birdie")

# Cores
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Fonte
font_path = 'assets/PressStart2P-Regular.ttf'
font = pygame.font.Font(font_path, 40)

# Classes do jogo
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y > 480:  # Limita a altura para não sair da tela
            self.y = 480
            self.velocity = 0

    def jump(self):
        self.velocity = self.jump_strength

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.width, self.height))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 60
        self.height = random.randint(100, 400)
        self.gap = 150
        self.speed = 5

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.height + self.gap, self.width, 600))

    def is_off_screen(self):
        return self.x + self.width < 0

# Função para desenhar a tela inicial
def draw_title_and_buttons():
    screen.fill(WHITE)  # Limpar a tela
    title_text = font.render("Flappy", True, (255, 255, 0))
    title_text2 = font.render("Birdie", True, ORANGE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(title_text2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2, 150))

    def draw_button(text, y_pos):
        button_text = font.render(text, True, WHITE)
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_text.get_width() // 2, y_pos, button_text.get_width() + 40, 60)
        pygame.draw.rect(screen, ORANGE, button_rect, border_radius=20)
        pygame.draw.rect(screen, RED, button_rect, 5)
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 15))

    draw_button("One Player", 250)
    draw_button("Exit", 320)

# Função para o jogo de um jogador
def start_game():
    bird = Bird(100, 250)
    pipes = [Pipe(600)]
    score = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.update()

        # Atualiza e desenha os canos
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)

            # Verifica colisões
            if bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width:
                if bird.y < pipe.height or bird.y + bird.height > pipe.height + pipe.gap:
                    running = False  # Game Over

            if pipe.is_off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe(600))
                score += 1  # Incrementa a pontuação

        bird.draw(screen)

        # Desenha a pontuação
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

# Função principal
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 250 <= mouse_pos[1] <= 300:
                    start_game()  # Inicia o jogo de um jogador
                elif 320 <= mouse_pos[1] <= 380:
                    pygame.quit()
                    sys.exit()

        draw_title_and_buttons()
        pygame.display.flip()

# Inicia o jogo
if __name__ == "__main__":
    main()
