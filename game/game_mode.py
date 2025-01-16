import pygame  # type: ignore
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
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Fonte
font_path = 'assets/fonts/PressStart2P-Regular.ttf'
font = pygame.font.Font(font_path, 40)

# Carregar e redimensionar imagens
bird_image = pygame.image.load('assets/birds/basic-yellow-bird.png')  # Imagem do pássaro
bird_image = pygame.transform.scale(bird_image, (30, 30))  # Redimensiona a imagem do pássaro
pipe_image = pygame.image.load('assets/pipes/green-pipe.png')  # Imagem do cano
pipe_image = pygame.transform.scale(pipe_image, (60, 260))  # Redimensiona a imagem do cano
bg_image = pygame.image.load('assets/backgrounds/mode-background.jpg')  # Imagem de fundo

# Inverte a imagem do cano superior
pipe_image_flipped = pygame.transform.flip(pipe_image, False, True)  # Inverte verticalmente

# Classes do jogo
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30  # Tamanho do pássaro
        self.height = 30  # Tamanho do pássaro
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
        screen.blit(bird_image, (self.x, self.y))  # Desenha a imagem do pássaro

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 60  # Largura dos canos
        self.height = random.randint(100, 350)  # Altura do cano superior
        self.gap = 150  # Gap fixo entre os canos
        self.speed = 5

        # Calcula a altura inferior com base na altura superior e no gap
        self.bottom_height = self.height + self.gap

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        # Desenha os canos como retângulos verdes (base de depuração)
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.height))  # Cano superior
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom_height, self.width, SCREEN_HEIGHT - self.bottom_height))  # Cano inferior

        # Desenha as imagens dos canos sobre os retângulos
        screen.blit(pipe_image_flipped, (self.x, self.height - pipe_image_flipped.get_height()))  # Cano superior invertido
        screen.blit(pipe_image, (self.x, self.bottom_height))  # Cano inferior

    def is_off_screen(self):
        return self.x + self.width < 0

# Função para o jogo de um jogador
def start_game():
    bird = Bird(100, 250)
    pipes = [Pipe(600)]
    score = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.update()

        # Verifica colisão com o teto e o chão
        if bird.y < -1 or bird.y == 480:
            running = False  # Game Over

        # Atualiza e desenha os canos
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)

            # Verifica colisões
            if bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width:
                if bird.y < pipe.height or bird.y + bird.height > pipe.bottom_height:
                    running = False  # Game Over

            if pipe.is_off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe(600))  # Adiciona um novo cano
                score += 1  # Incrementa a pontuação

        bird.draw(screen)

        # Desenha a pontuação
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

# Inicia o jogo
if __name__ == "__main__":
    start_game()
