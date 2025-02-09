import pygame # type: ignore
import sys
from PIL import Image # type: ignore
from game.game_mode import start_one_player_game, start_two_player_game, start_player_vs_machine_game

# Inicializa o Pygame
pygame.init()

# Configurações da tela (938x528)
SCREEN_WIDTH = 938
SCREEN_HEIGHT = 528
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Cria a tela com as dimensões
pygame.display.set_caption("Flappy Birdie")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Configurações da fonte
font_path = 'assets/fonts/PressStart2P-Regular.ttf'  # Caminho para a fonte
font = pygame.font.Font(font_path, 40)  # Fonte para o título (diminuído)
button_font = pygame.font.Font(font_path, 25)  # Fonte para os botões (diminuído)

# Função para carregar o GIF e dividir em frames
def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            # Converte cada frame em um Surface do Pygame
            frame = pygame.image.fromstring(gif.convert('RGB').tobytes(), gif.size, 'RGB')
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass  # Quando todos os quadros são lidos
    return frames

# Carregar os frames do GIF de fundo
bg_frames = load_gif_frames('assets/backgrounds/main-background.gif')

# Função para desenhar o título e botões
def draw_title_and_buttons():
    # Desenha o fundo (GIF)
    bg_frame = bg_frames[(pygame.time.get_ticks() // 100) % len(bg_frames)]  # Controla a troca de frames
    screen.blit(bg_frame, (0, 0))
    
    # Desenha o título com cores diferentes
    title_text1 = font.render("Flappy", True, YELLOW)  # "Flappy" amarelo
    title_text2 = font.render("Birdie", True, ORANGE)  # "Birdie" laranja
    screen.blit(title_text1, (SCREEN_WIDTH // 2 - (title_text1.get_width() + title_text2.get_width()) // 2 - 10, 80))
    screen.blit(title_text2, (SCREEN_WIDTH // 2 - (title_text1.get_width() + title_text2.get_width()) // 2 + title_text1.get_width() - 10, 80))

    # Função para desenhar botões
    def draw_button(text, y_pos):
        button_text = button_font.render(text, True, BLACK)
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_text.get_width() // 2, y_pos, button_text.get_width() + 40, 40)
        pygame.draw.rect(screen, ORANGE, button_rect, border_radius=20)  # Cor do botão e borda arredondada
        pygame.draw.rect(screen, BLACK, button_rect, 5)  # Borda preta
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))  # Ajustando o texto no botão

    # Desenha os botões (subir mais um pouco)
    draw_button("Um Jogador", 220)
    draw_button("Dois Jogadores", 270)
    draw_button("Jogador VS Máquina", 320)
    draw_button("Personalização", 370)  # Novo botão de personalização
    draw_button("Configurações", 420)
    draw_button("Sair", 470)

# Função principal
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 220 <= mouse_pos[1] <= 260:
                    start_one_player_game()  # Inicia o jogo de um jogador
                elif 270 <= mouse_pos[1] <= 310:
                    start_two_player_game()  # Iniciar "Dois Jogadores"
                elif 320 <= mouse_pos[1] <= 360:
                    start_player_vs_machine_game()  # Iniciar "Jogador Vs Maquina"
                elif 370 <= mouse_pos[1] <= 410:
                    pass  # Iniciar a tela de personalização
                elif 420 <= mouse_pos[1] <= 460:
                    pass  # Iniciar "Configurações"
                elif 470 <= mouse_pos[1] <= 510:
                    pygame.quit()  # Botão 'Sair' clicado
                    sys.exit()

        draw_title_and_buttons()
        pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 220 <= mouse_pos[1] <= 260:
                    start_one_player_game()  # Inicia o jogo de um jogador
                elif 270 <= mouse_pos[1] <= 310:
                    start_two_player_game()  # Iniciar "Dois Jogadores"
                elif 320 <= mouse_pos[1] <= 360:
                    start_player_vs_machine_game()  # Iniciar "Jogador Vs Maquina"
                elif 370 <= mouse_pos[1] <= 410:
                    pass  # Iniciar "Configurações"
                elif 420 <= mouse_pos[1] <= 460:
                    pygame.quit()  # Botão 'Sair' clicado
                    sys.exit()

        draw_title_and_buttons()
        pygame.display.flip()

# Inicia o jogo
if __name__ == "__main__":
    main()
