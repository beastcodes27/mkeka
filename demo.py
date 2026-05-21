import pygame
import random
import os

# 1. INITIALIZATION
pygame.font.init()

S_WIDTH = 800
S_HEIGHT = 700
PLAY_WIDTH = 300  
PLAY_HEIGHT = 600 
BLOCK_SIZE = 30

TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = S_HEIGHT - PLAY_HEIGHT

# PAKIA PICHA YA BACKGROUND
try:
    BG_IMAGE = pygame.image.load("background.png")
    BG_IMAGE = pygame.transform.scale(BG_IMAGE, (S_WIDTH, S_HEIGHT))
except:
    BG_IMAGE = pygame.Surface((S_WIDTH, S_HEIGHT))
    BG_IMAGE.fill((30, 30, 30))

# MIFUMO YA VIPANDE (Tetrominoes) - (Imehifadhiwa kama mwanzo)
S = [['.....', '.....', '..00.', '.00..', '.....'], ['.....', '..0..', '..00.', '...0.', '.....']]
Z = [['.....', '.....', '.00..', '..00.', '.....'], ['.....', '..0..', '.00..', '.0..', '.....']]
I = [['..0..', '..0..', '..0..', '..0..', '.....'], ['.....', '0000.', '.....', '.....', '.....']]
O = [['.....', '.....', '.00..', '.00..', '.....']]
J = [['.....', '.0...', '.000.', '.....', '.....'], ['.....', '..00.', '..0..', '..0..', '.....'], ['.....', '.....', '.000.', '...0.', '.....'], ['.....', '..0..', '..0..', '.00..', '.....']]
L = [['.....', '...0.', '.000.', '.....', '.....'], ['.....', '..0..', '..0..', '..00.', '.....'], ['.....', '.....', '.000.', '.0...', '.....'], ['.....', '.00..', '..0..', '..0..', '.....']]
T = [['.....', '..0..', '.000.', '.....', '.....'], ['.....', '..0..', '..00.', '..0..', '.....'], ['.....', '.....', '.000.', '..0..', '.....'], ['.....', '..0..', '.00..', '..0..', '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def get_high_score():
    if not os.path.exists("highscore.txt"): return 0
    try:
        with open("highscore.txt", "r") as f: return int(f.read())
    except: return 0

def save_high_score(new_score):
    current_high = get_high_score()
    if new_score > current_high:
        with open("highscore.txt", "w") as f: f.write(str(new_score))

def create_grid(locked_pos={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos: grid[i][j] = locked_pos[(j,i)]
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0': positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions): positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1: return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1: return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color, offset=0):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (S_WIDTH/2 - (label.get_width()/2), S_HEIGHT/2 - label.get_height()/2 + offset))

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try: del locked[(j,i)]
                except: continue
    if inc > 0:
        for key in sorted(list(locked.keys()), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_window(surface, grid, score=0, high_score=0):
    surface.blit(BG_IMAGE, (0, 0)) 
    overlay = pygame.Surface((PLAY_WIDTH, PLAY_HEIGHT))
    overlay.set_alpha(180) 
    overlay.fill((0,0,0))
    surface.blit(overlay, (TOP_LEFT_X, TOP_LEFT_Y))

    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS ', 1, (255, 255, 255))
    surface.blit(label, (S_WIDTH / 2 - (label.get_width() / 2), 30))

    s_font = pygame.font.SysFont('comicsans', 30)
    surface.blit(s_font.render(f'Score: {score}', 1, (255, 255, 255)), (TOP_LEFT_X + PLAY_WIDTH + 20, TOP_LEFT_Y + 50))
    surface.blit(s_font.render(f'Best: {high_score}', 1, (255, 255, 0)), (TOP_LEFT_X + PLAY_WIDTH + 20, TOP_LEFT_Y + 100))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (TOP_LEFT_X, TOP_LEFT_Y + i*BLOCK_SIZE), (TOP_LEFT_X+PLAY_WIDTH, TOP_LEFT_Y + i*BLOCK_SIZE))
    for j in range(10):
        pygame.draw.line(surface, (128,128,128), (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j*BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)
    pygame.display.update()

# --- HII NDIO GAME ENGINE KUU ---
def play_game():
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    paused = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    score = 0
    high_score = get_high_score()

    while run:
        grid = create_grid(locked_positions)
        if not paused:
            fall_time += clock.get_rawtime()
            clock.tick()
            if fall_time/1000 > fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not valid_space(current_piece, grid) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True
        else:
            clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Rudi Menu
                    run = False
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if not paused:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid): current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid): current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid): current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        current_piece.rotation += 1
                        if not valid_space(current_piece, grid): current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)
        if not paused:
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1: grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 100
            save_high_score(score)

        draw_window(win, grid, score, high_score)
        if paused:
            draw_text_middle(win, "PAUSED", 80, (255, 255, 0))
            pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "GAME OVER", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False # Itarudi kwenye main_menu()

def main_menu():
    run = True
    while run:
        win.blit(BG_IMAGE, (0, 0))
        # Kiza kidogo cha Home Screen
        dark_surface = pygame.Surface((S_WIDTH, S_HEIGHT))
        dark_surface.set_alpha(150)
        dark_surface.fill((0, 0, 0))
        win.blit(dark_surface, (0, 0))

        draw_text_middle(win, 'TETRIS TZ', 100, (255, 255, 255), -150)
        draw_text_middle(win, f'HIGH SCORE: {get_high_score()}', 40, (255, 215, 0), -50)
        draw_text_middle(win, 'Press SPACE to Start', 50, (0, 255, 0), 50)
        draw_text_middle(win, 'Press ESC to Quit', 30, (255, 0, 0), 120)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_game() # Anza Game
                if event.key == pygame.K_ESCAPE:
                    run = False

    pygame.quit()

# KUENDESHA GAME
win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('Tetris TZ')
main_menu()
