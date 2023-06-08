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

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

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

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100 
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3	and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	# Center column preference
	center_array = [int(i) for i in list(board[:,COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	# Horizontal score
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]

			score += evaluate_window(window, piece)

	# Vertical score
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]

			score += evaluate_window(window, piece)


	# Positive diagonal score
	for r in range (ROW_COUNT-3):
		for c in range (COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			
			score += evaluate_window(window, piece)


	# Negative diagonal score
	for r in range(ROW_COUNT-3):
		for c in range (COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			
			score += evaluate_window(window, piece)


	return score			

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)

	return valid_locations		

def pick_best_move(board, piece):
	valid_locations = get_valid_locations(board)
	best_score = -1000
	best_col = random.choice(valid_locations)

	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy() #To create new memory location to pass drop_piece
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board,piece)

		if score > best_score:
			best_score = score
			best_col = col

	return best_col		


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

				
	# AI Input
	if turn == AI and not game_over:

		#col = random.randint(0, COLUMN_COUNT-1)
		col = pick_best_move(board, AI_PIECE)

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
		pygame.time.wait(3000)
