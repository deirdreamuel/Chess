# import pygame libary
from re import error
import pygame
from pygame.locals import *

# import chess libary
import chess

# import numpy library
import numpy as np

# initialize game
pygame.init()

# create chess board
chess_game = chess.Board()

# screen variables
SCREEN_WIDTH = 400 
SCREEN_HEIGHT = 400
TILE_SIZE = SCREEN_WIDTH / 8

# color variables
BLACK = (0, 0, 0)
WHITE = (239, 239, 232)
RED = (255, 0, 0)

YELLOW = (200, 194, 114)
GREEN = (15, 22, 17)

# function to setup chess board tiles
def setup_chess_board(chess_game: chess.Board, screen: pygame.surface, flip_board: bool, chess_move: str):
    tile_outline = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    draw_chess_board(chess_game, tile_outline, flip_board, chess_move)
    #draw_chess_outline(tile_outline, YELLOW)

    screen.blit(tile_outline, (0, 0))

# function to draw chessboard
def draw_chess_board(chess_game: chess.Board, screen: pygame.surface, flipped: bool, current_move: str):
    
    if not current_move:
        pass
    
    if flipped:
        screen.fill(WHITE)
        chess_color_1 = GREEN
        chess_color_2 = WHITE
    else:
        screen.fill(GREEN)
        chess_color_1 = WHITE
        chess_color_2 = GREEN

    chess_color_3 = YELLOW


    for width in range(0, 8):
        for height in range(0, 8):
            rect = ((width * TILE_SIZE, height * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
            
            if width %  2 and height % 2:
                pygame.draw.rect(screen, chess_color_1, rect)

            if not height % 2 and not width % 2:
                pygame.draw.rect(screen, chess_color_1, rect)

    if len(current_move) == 2:
        allowed_moves = check_move(chess_game, current_move)

        next_tiles = []
        for i in allowed_moves:
            next_tiles.append(i[2:4])

        next_tile_pos = []
        for i in next_tiles:
            next_tile_pos = chess.parse_square(i)

            rect = (((int(next_tile_pos) % 8 )* TILE_SIZE, SCREEN_HEIGHT - ((int(next_tile_pos) // 8) + 1) * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, chess_color_3, rect)



# function to draw tile outline
def draw_chess_outline(screen: pygame.surface, outline_color):
    line_width = 2

    for line in range(1, 8):
        pygame.draw.line(screen, outline_color, (0, line*TILE_SIZE), (SCREEN_WIDTH, line*TILE_SIZE), line_width)
        pygame.draw.line(screen, outline_color, (line*TILE_SIZE, 0), (line*TILE_SIZE, SCREEN_WIDTH), line_width)

    pygame.draw.line(screen, outline_color, (0, 0), (SCREEN_WIDTH, 0), line_width)
    pygame.draw.line(screen, outline_color, (0, 0), (0, SCREEN_HEIGHT), line_width)

    pygame.draw.line(screen, outline_color, (0, SCREEN_WIDTH-1), (SCREEN_WIDTH-1, SCREEN_HEIGHT-1), line_width)
    pygame.draw.line(screen, outline_color, (SCREEN_WIDTH-1, 0), (SCREEN_WIDTH-1, SCREEN_HEIGHT-1), line_width)




# function to get current chessboard state
def get_chess_state(chess_game: chess.Board):
    chess_arr = []
    for i in range(64):
        piece = str(chess_game.piece_at(i))
        if (piece == 'None'): piece = ' '
        
        chess_arr.append(piece)

    chess_arr = np.array(chess_arr)
    chess_arr.resize((8,8))
    chess_arr.tolist()

    return chess_arr




# display chess set and pieces
# --- 
import os


def setup_chess_pieces(scale: int):
    pieces_key = ['K', 'Q', 'R', 'B', 'N','P','k', 'q', 'r', 'b', 'n','p']
    
    pieces = {}
    
    try:
        for key in pieces_key:
            path = os.getcwd() + "/pieces/"

            path = path + key
            
            if (key.islower()):
                path = path + "_"
                
            path = path + ".png"

            piece_img = pygame.image.load(path)
            piece_img = pygame.transform.scale(piece_img, (int(TILE_SIZE), int(TILE_SIZE)))

            pieces[key] = piece_img

        pieces["scale"] = scale
            
    except:
        "Error Loading chess pieces!"

    return pieces


# function to draw chess state
def draw_chess_state(chess_game: chess.Board):
    tile_list = []

    chess_arr = get_chess_state(chess_game)

    for x, i in zip(range(8), (range(8))):
        for y, j in zip(range(8), reversed(range(8))):
            
            if chess_arr[j,i] == ' ':
                continue

            chess_tile =  pieces[chess_arr[j, i]]
    
            chess_tile = pygame.transform.scale(chess_tile, (int(TILE_SIZE - pieces["scale"]), int(TILE_SIZE - pieces["scale"])))

            chess_rect = chess_tile.get_rect()
            chess_rect.x = x * TILE_SIZE + (pieces["scale"] // 2)
            chess_rect.y = y * TILE_SIZE + (pieces["scale"] // 2)

            tile = (chess_tile, chess_rect)
            tile_list.append(tile)

    for tile in tile_list:
        screen.blit(tile[0], tile[1])


# function to get chess tile 
def get_chess_tile(x: int, y: int):
    chess_tile_x = int(x // TILE_SIZE)
    chess_tile_y = int(y // TILE_SIZE)

    chess_tile_letter : str = chr(ord('a') + chess_tile_x)
    
    chess_tile_number : int = 0
    chess_tile_number = 8 - (chess_tile_number + chess_tile_y)

    return (chess_tile_letter + str(chess_tile_number))



'''
    arguments: chess_game < chess.Board() >
    use: prints a list of valid moves
'''
def print_valid_moves(chess_game: chess.Board):
    print("VALID MOVES:\n uci - san")
    for move in chess_game.legal_moves:
        print(chess_game.uci(move))

'''
    arguments: chess_game < chess.Board() >
    use: returns a list of valid moves
'''
def get_valid_moves(chess_game: chess.Board):
    valid_moves = []
    for move in chess_game.legal_moves:
        valid_moves.append(chess_game.uci(move))

    return valid_moves


'''
    arguments: chess_game < chess.Board() >
    use: checks if move is valid
'''
def check_move(chess_game: chess.Board, move: str):
    valid_moves = get_valid_moves(chess_game)    
    find_move = [s for s in valid_moves if move in s[:2]]
    
    return find_move


#------- MAIN --------
# setup chess piece tiles
SCALE = 20
pieces = setup_chess_pieces(scale=SCALE)

# setup pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CHESS")

# setup chess board design
setup_chess_board(chess_game, screen, False, "")

# get current chess state
chess_arr = get_chess_state(chess_game)

draw_chess_state(chess_game)

# run pygame 
run = True


chess_move = ""

while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            chess_move = chess_move + get_chess_tile(x, y)

            try:
                move = chess.Move.from_uci(chess_move)
            except:
                move = chess.Move.null()

            if len(chess_move) == 2:

                if not check_move(chess_game, chess_move):
                    chess_move = ""

                setup_chess_board(chess_game, screen, False, chess_move)
                draw_chess_state(chess_game)
        

            if len(chess_move) >= 4:
                valid_moves = get_valid_moves(chess_game)

                if str(move) in valid_moves: 
                    chess_game.push(move)

                if str(move) +'q' in valid_moves: 
                    chess_game.push(chess.Move.from_uci(str(move) + 'q'))

                chess_move = ""
                setup_chess_board(chess_game, screen, False, chess_move)
                draw_chess_state(chess_game)
        
    pygame.display.update()

pygame.quit()

