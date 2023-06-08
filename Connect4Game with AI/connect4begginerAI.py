import numpy as np
import pygame
import sys
import math
import random

BLUE = (0, 0, 235)
BLACK = (0, 0, 0)
RED = (235, 0, 0)
YELLOW = (235, 235, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def print_board(board):
	print (np.flip(board, 0))

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board [ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def winning_move(board, piece):
	# Check horizontal connections for win
	for c in range (COLUMN_COUNT-3):
		for r in range (ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical connections for win
	for c in range (COLUMN_COUNT):
		for r in range (ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positive slope diagonals for win
	for c in range (COLUMN_COUNT-3):
		for r in range (ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True
	
	# Check negative slope diagonals for win	
	for c in range (COLUMN_COUNT-3):
		for r in range (3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True	


def draw_board(board):
	for c in range (COLUMN_COUNT):
		for r in range (ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
	for c in range (COLUMN_COUNT):
		for r in range (ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height - int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)

	pygame.display.update()		

board = create_board()
print_board(board)
game_over = False
turn = random.randint(PLAYER, AI)

pygame.init()

SQUARE_SIZE = 80

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE

size = (width, height)

RADIUS = int((SQUARE_SIZE/2) - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("ROG FONTS", 50)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE/2)), RADIUS)
			
		pygame.display.update()		

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE_SIZE))

			# Player1 Input
			if turn == PLAYER:

				posx = event.pos[0]
				col = int(math.floor(posx/SQUARE_SIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if winning_move(board, PLAYER_PIECE):
						label = myfont.render("YOU WIN!", 1, RED)
						screen.blit(label, (145,5))
						game_over = True

					print_board(board)
					draw_board(board)

					turn += 1
					turn = turn % 2	

				
	# Player2 Input
	if turn == AI and not game_over:

		col = random.randint(0, COLUMN_COUNT-1)

		if is_valid_location(board, col):
			pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE):
				label = myfont.render("YOU LOSE!", 1, YELLOW)
				screen.blit(label, (125,6))
				game_over = True


			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(5000)
