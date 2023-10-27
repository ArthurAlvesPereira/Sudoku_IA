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

# Variáveis para o relatório
attempt_count = 0
successful_attempts = 0
start_time = time.time()

# Função para desenhar o tabuleiro
def draw_board(board):
    screen.fill(WHITE)  
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_value = board[i][j]
            if cell_value != 0:
                if example_board[i][j] == 0:
                    text_color = BLUE  
                else:
                    text_color = BLACK  
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
    for i in range(GRID_SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


# nova funcao: encontrar a próxima célula vazia com base na heuristica MRV (Menor Número de Opções Restantes)
def find_empty_cell(board):
    minimo_opcoes = float('inf')
    empty_cell = None

    # loop para procurar qual linha/coluna tem mais elementos, para começar pela celula com menos possibilidades
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                # pega um no aleatorio, verifica se eh valido para aquela celula
                options = [num for num in range(1, 10) if is_valid(board, row, col, num)]
                # quantidade de opções possiveis para aquela celula
                num_options = len(options)

                # comparação para ver se aquela celula é a com menos possibilidades
                if num_options < minimo_opcoes:
                    minimo_opcoes = num_options
                    empty_cell = (row, col)

    # retorna a célula com a menor quantidade de opções (ou seja, linha/coluna com mais elementos)
    return empty_cell

def solve_sudoku(board):
    global attempt_count
    global successful_attempts

    # chamada da função heuristica MRV
    empty_cell = find_empty_cell(board)

    if not empty_cell:
        # não há mais células vazias, o tabuleiro está resolvido
        return True

    row, col = empty_cell

    for num in range(1, 10):
        attempt_count += 1
        if is_valid(board, row, col, num):
            successful_attempts += 1
            board[row][col] = num
            draw_board(board)
            pygame.display.flip()
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # desfazer a tentativa, retroceder (backtracking em si)

    return False


# Tabuleiro de exemplo (0 representa células vazias)
example_board = [
    [0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 0, 0, 0, 0, 3],
    [0, 7, 4, 0, 8, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 0, 0, 2],
    [0, 8, 0, 0, 4, 0, 0, 1, 0],
    [6, 0, 0, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 7, 8, 0],
    [5, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0]

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
    
if not solved:
    solved = solve_sudoku(board)
print(f'Total de tentativas: {attempt_count}')
print(f'Tempo gasto: {time.time() - start_time} segundos')
print(f'Tentativas bem-sucedidas: {successful_attempts}')

# Encerrando o Pygame
pygame.quit()
sys.exit()
