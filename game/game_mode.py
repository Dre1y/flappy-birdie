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
        # Desenha as imagens dos canos
        screen.blit(pipe_image_flipped, (self.x, self.height - pipe_image_flipped.get_height()))  # Cano superior invertido
        screen.blit(pipe_image, (self.x, self.bottom_height))  # Cano inferior

    def is_off_screen(self):
        return self.x + self.width < 0
    
# Lógica da IA MELHORADA: Quando pular (Em andamento)
def ai_jump_logic(bird, pipes):
    """Função para a IA decidir quando pular"""
    bird_center = bird.y + bird.height // 2  # Centro do pássaro
    closest_pipe = None
    for pipe in pipes:
        if pipe.x > bird.x and pipe.x < bird.x + 300:  # Olha para os canos próximos
            closest_pipe = pipe
            break

    if closest_pipe:
        # Verifica se o espaço entre os canos está ficando pequeno
        gap_middle = closest_pipe.height + closest_pipe.gap // 2
        if bird_center < gap_middle:
            # Se o pássaro está abaixo do meio do gap, ele tenta subir
            bird.jump()

# Função para o jogo de um jogador
def start_one_player_game():
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
            # Exibe a mensagem de Game Over
            game_over_text = font.render("Game Over", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
                    
            pygame.time.delay(1000)  # Espera 1 segundo
            running = False  # Game Over

        # Atualiza e desenha os canos
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)

            # Verifica colisões
            if bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width:
                if bird.y < pipe.height or bird.y + bird.height > pipe.bottom_height:
                    # Exibe a mensagem de Game Over
                    game_over_text = font.render("Game Over", True, BLACK)
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
                    pygame.display.flip()

                    pygame.time.delay(1000)  # Espera 1 segundo
                    running = False  # Game Over

        # Adiciona novos canos à medida que os antigos saem da tela
        if pipes[-1].x + pipes[-1].width < SCREEN_WIDTH - 300:  # Adiciona um novo cano a cada 300 pixels
            pipes.append(Pipe(SCREEN_WIDTH))

        # Remove os canos que saíram da tela e incrementa o score
        for pipe in pipes:
            if pipe.is_off_screen():
                score += 1  # Incrementa a pontuação quando um cano sai da tela

        # Remove os canos que saíram da tela
        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

        bird.draw(screen)

        # Desenha a pontuação
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

def start_two_player_game():
    bird1 = Bird(100, 250)  # Jogador 1
    bird2 = Bird(200, 250)  # Jogador 2
    pipes = [Pipe(600)]
    score1 = 0
    score2 = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(bg_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  # Tecla do Jogador 1
                    bird1.jump()
                if event.key == pygame.K_p:  # Tecla do Jogador 2
                    bird2.jump()

        bird1.update()
        bird2.update()

        # Verifica colisão com o teto e o chão para ambos os jogadores
        if bird1.y < -1 or bird1.y == 480:
            # Game Over Jogador 1
            game_over_text = font.render("Game Over - Jogador 1", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(1000)  # Espera 1 segundo
            running = False  # Game Over Jogador 1

        if bird2.y < -1 or bird2.y == 480:
            # Game Over Jogador 2
            game_over_text = font.render("Game Over - Jogador 2", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(1000)  # Espera 1 segundo
            running = False  # Game Over Jogador 2

        # Atualiza e desenha os canos
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)

            # Verifica colisões para ambos os jogadores
            if bird1.x + bird1.width > pipe.x and bird1.x < pipe.x + pipe.width:
                if bird1.y < pipe.height or bird1.y + bird1.height > pipe.bottom_height:
                    game_over_text = font.render("Game Over - Jogador 1", True, BLACK)
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.delay(1000)  # Espera 1 segundo
                    running = False  # Game Over Jogador 1

            if bird2.x + bird2.width > pipe.x and bird2.x < pipe.x + pipe.width:
                if bird2.y < pipe.height or bird2.y + bird2.height > pipe.bottom_height:
                    game_over_text = font.render("Game Over - Jogador 2", True, BLACK)
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.delay(1000)  # Espera 1 segundo
                    running = False  # Game Over Jogador 2

        # Adiciona novos canos à medida que os antigos saem da tela
        if pipes[-1].x + pipes[-1].width < SCREEN_WIDTH - 300:
            pipes.append(Pipe(SCREEN_WIDTH))

        # Remove os canos que saíram da tela e incrementa a pontuação
        for pipe in pipes:
            if pipe.is_off_screen():
                score1 += 1  # Incrementa a pontuação para o Jogador 1
                score2 += 1  # Incrementa a pontuação para o Jogador 2

        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

        bird1.draw(screen)
        bird2.draw(screen)

        # Desenha a pontuação
        score_text1 = font.render(f"Score Jogador 1: {score1}", True, BLACK)
        score_text2 = font.render(f"Score Jogador 2: {score2}", True, BLACK)
        screen.blit(score_text1, (10, 10))
        screen.blit(score_text2, (10, 50))

        pygame.display.flip()
        clock.tick(30)

def start_player_vs_machine_game():
    bird = Bird(100, 250)  # Jogador
    bird_ai = Bird(200, 250)  # Máquina
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
                bird.jump()  # Jogador pula com a tecla espaço

        bird.update()

        # A máquina toma decisões automáticas
        if bird_ai.y < pipes[0].height or bird_ai.y + bird_ai.height > pipes[0].bottom_height:
            bird_ai.jump()  # A máquina pula se necessário

        bird_ai.update()

        # Verifica colisão com o teto e o chão para ambos
        if bird.y < -1 or bird.y == 480:
            game_over_text = font.render("Game Over - Jogador", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(1000)  # Espera 1 segundo
            running = False  # Game Over Jogador

        if bird_ai.y < -1 or bird_ai.y == 480:
            game_over_text = font.render("Game Over - Máquina", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(1000)  # Espera 1 segundo
            running = False  # Game Over Máquina

        # Atualiza e desenha os canos
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)

            # Verifica colisões
            if bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width:
                if bird.y < pipe.height or bird.y + bird.height > pipe.bottom_height:
                    game_over_text = font.render("Game Over - Jogador", True, BLACK)
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.delay(1000)  # Espera 1 segundo
                    running = False  # Game Over Jogador

            if bird_ai.x + bird_ai.width > pipe.x and bird_ai.x < pipe.x + pipe.width:
                if bird_ai.y < pipe.height or bird_ai.y + bird_ai.height > pipe.bottom_height:
                    game_over_text = font.render("Game Over - Máquina", True, BLACK)
                    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.delay(1000)  # Espera 1 segundo
                    running = False  # Game Over Máquina

        # Adiciona novos canos
        if pipes[-1].x + pipes[-1].width < SCREEN_WIDTH - 300:
            pipes.append(Pipe(SCREEN_WIDTH))

        # Remove canos e incrementa o score
        for pipe in pipes:
            if pipe.is_off_screen():
                score += 1  # Incrementa a pontuação

        pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

        bird.draw(screen)
        bird_ai.draw(screen)

        # Desenha a pontuação
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)
