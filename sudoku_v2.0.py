import pygame
import sys
import time

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)  # Cinza para números originais
BLUE = (0, 0, 255)       # Azul para números inseridos

# Tamanho das células e das grades
CELL_SIZE = SCREEN_WIDTH // 9
GRID_SIZE = 9

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku Solver")

# Fonte para os números
font = pygame.font.Font(None, 36)

# Função para desenhar o tabuleiro
def draw_board(board):
    screen.fill(WHITE)  # Preenche a tela com branco
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_value = board[i][j]
            if cell_value != 0:
                if example_board[i][j] == 0:
                    text_color = BLUE  # Azul para números inseridos
                else:
                    text_color = GRAY  # Cinza para números originais
                text_surface = font.render(str(cell_value), True, text_color)
                text_rect = text_surface.get_rect()
                text_rect.center = (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2)
                screen.blit(text_surface, text_rect)

    for i in range(1, GRID_SIZE):
        line_thickness = 2
        if i % 3 == 0:
            line_thickness = 4
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT), line_thickness)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), line_thickness)

def is_valid(board, row, col, num):
    # Verifica se o número já está na linha ou coluna
    for i in range(GRID_SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Verifica se o número já está na sub-grade 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        draw_board(board)  # Atualizar a tela
                        pygame.display.flip()
                        time.sleep(0.05)  # Pequeno atraso para exibição
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# Tabuleiro de exemplo (0 representa células vazias)
example_board = [
    [1, 0, 9, 6, 8, 0, 0, 5, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 7],
    [0, 6, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0],
    [3, 0, 8, 0, 1, 0, 0, 9, 0],
    [0, 0, 0, 0, 0, 9, 5, 0, 0],
    [0, 5, 0, 0, 6, 0, 0, 0, 0],
    [0, 4, 0, 0, 0, 0, 0, 3, 0],
    [6, 0, 3, 8, 0, 0, 2, 0, 0]
]

# Copiar o tabuleiro de exemplo para a variável de trabalho
board = [row[:] for row in example_board]

# Loop principal do jogo
running = True
solved = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not solved:
        solved = solve_sudoku(board)

    draw_board(board)
    pygame.display.flip()

# Encerrando o Pygame
pygame.quit()
sys.exit()
