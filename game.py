import pygame
import sys
from PIL import Image

# Inicializa o Pygame
pygame.init()

# Configurações da tela (ocupar toda a área da tela sem ser fullscreen)
screen_info = pygame.display.Info()  # Obtém informações da tela
SCREEN_WIDTH = screen_info.current_w  # Largura da tela
SCREEN_HEIGHT = screen_info.current_h  # Altura da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Cria a tela com as dimensões
pygame.display.set_caption("Flappy Birdie")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Configurações da fonte
font_path = 'assets/PressStart2P-Regular.ttf'  # Caminho para a fonte
font = pygame.font.Font(font_path, 60)  # Fonte para o título
button_font = pygame.font.Font(font_path, 40)  # Fonte para os botões

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
bg_frames = load_gif_frames('assets/background.gif')

# Função para desenhar o título e botões
def draw_title_and_buttons():
    # Desenha o fundo (GIF)
    bg_frame = bg_frames[(pygame.time.get_ticks() // 100) % len(bg_frames)]  # Controla a troca de frames
    screen.blit(bg_frame, (0, 0))
    
    # Desenha o título com gradiente de cor
    title_text = font.render("Flappy Birdie", True, ORANGE)
    title_text2 = font.render("Flappy Birdie", True, RED)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(title_text2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2, 160))  # Efeito sobreposto

    # Função para desenhar botões
    def draw_button(text, y_pos):
        button_text = button_font.render(text, True, BLACK)
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_text.get_width() // 2, y_pos, button_text.get_width() + 40, 60)
        pygame.draw.rect(screen, ORANGE, button_rect, border_radius=20)  # Cor do botão e borda arredondada
        pygame.draw.rect(screen, BLACK, button_rect, 5)  # Borda preta
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 15))  # Ajustando o texto no botão

    # Desenha os botões
    draw_button("Um Jogador", 250)
    draw_button("Dois Jogadores", 320)
    draw_button("Jogador Vs Maquina", 390)
    draw_button("Configurações", 460)
    draw_button("Sair", 530)

# Função para gerenciar eventos e interações
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Verificar cliques nos botões
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 250 <= mouse_pos[1] <= 300:
                print("Botão 'Um Jogador' clicado")
            elif 320 <= mouse_pos[1] <= 370:
                print("Botão 'Dois Jogadores' clicado")
            elif 390 <= mouse_pos[1] <= 440:
                print("Botão 'Jogador Vs Maquina' clicado")
            elif 460 <= mouse_pos[1] <= 510:
                print("Botão 'Configurações' clicado")
            elif 530 <= mouse_pos[1] <= 580:
                pygame.quit()
                sys.exit()

# Função principal
def main():
    while True:
        # Gerenciar eventos
        handle_events()

        # Desenhar título e botões
        draw_title_and_buttons()

        # Atualiza a tela
        pygame.display.flip()

# Inicia o jogo
if __name__ == "__main__":
    main()
