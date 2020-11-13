import numpy as np
import pygame
import sys,copy,random
import math

GREEN = (0,255,0)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
SQUARESIZE = 80
HEIGHT = 6
WIDTH = 7
width = WIDTH * SQUARESIZE
height = HEIGHT* SQUARESIZE+SQUARESIZE
size = (width, height)
R = int(SQUARESIZE/2 - 5)#radius for circle
HUMAN = 'human'
COMPUTER = 'computer'


def main(argv):
		
	board = make_board()
	turn = HUMAN
	pygame.init()
	screen = pygame.display.set_mode(size)
	draw_board(board,screen)
	pygame.display.update()
	winning=False
	if sys.argv[1]=="-AI1":
		while True :
			if is_full(board):
				break
			if winning:
				for event in pygame.event.get():
					 # event handling loop
					if event.type == pygame.QUIT:
						pygame.quit()

						sys.exit()
					elif event.type == pygame.MOUSEBUTTONDOWN:#click to restart the game
						board = make_board()
						draw_board(board,screen)
						pygame.display.update()
						winning=False
			# event handling loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()		
				pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
				if event.type == pygame.MOUSEMOTION:
					posx = event.pos[0]
					if turn == HUMAN and winning==False:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), R)

				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					# Ask for Player  Input
					if turn ==HUMAN:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))
						if is_valid_move(board, col):
							row = get_next_empty_row(board, col)
							make_move(board, 1,row, col)#Human representation is 1
							turn=COMPUTER
							if is_winning(board, 1):#if human wins
								a =pygame.font.SysFont("monospace", 20).render("Player wins,click to replay", 1, RED)
								screen.blit(a, (50,10))
								winning=True
								turn=HUMAN

				#computer's turn
				if turn ==COMPUTER:				
					if is_valid_move(board, col):
						col=getComputerMove1(board)
						row = get_next_empty_row(board, col)
						make_move(board, 2,row, col)#computer representatin is 2
						turn=HUMAN
						if is_winning(board, 2):
							a =  pygame.font.SysFont("monospace", 20).render("COMPUTER wins,click to replay", 1, BLUE)
							screen.blit(a, (50,10))
							winning=True
							turn=HUMAN
				draw_board(board,screen)
	elif sys.argv[1]=="-player":
		while True :
			if is_full(board):
				break
			if winning:#handle winning case
				for event in pygame.event.get():
					 # event handling loop
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					elif event.type == pygame.MOUSEBUTTONDOWN:#click to restart the game
						board = make_board()
						draw_board(board,screen)
						pygame.display.update()
						winning=False
			# event handling loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()			
				
				pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
				
				if event.type == pygame.MOUSEMOTION:
					posx = event.pos[0]
					if turn == HUMAN and winning==False:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), R)
					else:
						pygame.draw.circle(screen, BLUE, (posx, int(SQUARESIZE/2)), R)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					# Ask for Player1 
					if turn ==HUMAN:
						posx = event.pos[0]#get the cursor position
						col = int(math.floor(posx/SQUARESIZE))#change into column position
						if is_valid_move(board, col):
							row = get_next_empty_row(board, col)
							make_move(board, 1,row, col)#player1 representation is 1
							turn=""
							if is_winning(board, 1):#if player1 wins
								a =pygame.font.SysFont("monospace", 20).render("Player 1 wins,click to replay", 1, RED)
								screen.blit(a, (50,10))
								winning=True
								turn=HUMAN

					#player2 's turn
					else:	
							posx = event.pos[0]
							col=int(math.floor(posx/SQUARESIZE))			
							if is_valid_move(board, col):
								row = get_next_empty_row(board, col)
								make_move(board, 2,row, col)#player2 representatin is 2
								turn=HUMAN
								if is_winning(board, 2):#if player2 wins
									a =  pygame.font.SysFont("monospace", 20).render("player2 wins,click to replay", 1, BLUE)
									screen.blit(a, (50,10))
									winning=True
									turn=HUMAN
					draw_board(board,screen)




def make_move(board, player_type,row, col):
	board[row][col] = player_type

def make_board():
	w=WIDTH
	h=HEIGHT
	board_matrix = [[0 for x in range(w)] for y in range(h)]
	return board_matrix


def is_full(board):
	for x in range(WIDTH):
		for y in range(HEIGHT):
			if board[x][y] == 0:
				return False
	return True

def is_valid_move(board, col):#check if it is valid move
	if col < 0 or col >= WIDTH or board[HEIGHT-1][col] != 0:
		return False
	return True
	 

def get_next_empty_row(board, col):
	for r in range(HEIGHT):
		if board[r][col] == 0:
			return r


def is_winning(board, player_type):

	# Check vertical 
	for c in range(WIDTH):
		for r in range(HEIGHT-3):
			if board[r][c] == player_type and board[r+1][c] == player_type and board[r+2][c] == player_type and board[r+3][c] == player_type:
				return True

	# Check horizontal 
	for c in range(WIDTH-3):
		for r in range(HEIGHT):
			if board[r][c] == player_type and board[r][c+1] == player_type and board[r][c+2] == player_type and board[r][c+3] == player_type:
				return True

	# Check / diaganols
	for c in range(WIDTH-3):
		for r in range(HEIGHT-3):
			if board[r][c] == player_type and board[r+1][c+1] == player_type and board[r+2][c+2] == player_type and board[r+3][c+3] == player_type:
				return True

	# Check \ diaganols
	for c in range(WIDTH-3):
		for r in range(3, HEIGHT):
			if board[r][c] == player_type and board[r-1][c+1] == player_type and board[r-2][c+2] == player_type and board[r-3][c+3] == player_type:
				return True

def draw_board(board,screen):
	for c in range(WIDTH):
		for r in range(HEIGHT):
			pygame.draw.rect(screen, GREEN, (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE))

			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), R)
	
	for c in range(WIDTH):
		for r in range(HEIGHT):	

			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), R)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), R)
	
	pygame.display.update()


def getComputerMove1(board):
	possible_moves = getPossibleMoves1(board, 2)
	bestMoveValue = -1000#initialise value
	bestMoves = []
	for i in range(WIDTH):
		if possible_moves[i] > bestMoveValue:
			bestMoveValue = possible_moves[i]
	for i in range(len(possible_moves)):
		if possible_moves[i] == bestMoveValue:
			bestMoves.append(i)
	return random.choice(bestMoves)

#potential move for the AI using the first method that look ahead one step ahead(not so smart!)
def getPossibleMoves1(board, player_type):

	if player_type==1:
		enemy=2
	else:
		enemy=1
	moves_value=np.zeros(WIDTH)
	for m in range(WIDTH):
		temp_board=copy.deepcopy(board)
		if not is_valid_move(board,m):
			continue
		r=get_next_empty_row(temp_board,m)
		make_move(temp_board,player_type,r,m)
		if is_winning(temp_board,player_type):#if winning move it gets 100 score
			moves_value[m]=100
			break
		else:#look at other player's counter move 
			if is_full(temp_board):
				moves_value[m] = 0
			else:
				for enemy_move in range(WIDTH):
					temp_board2=copy.deepcopy(temp_board)
					if not is_valid_move(temp_board2,enemy_move):
						continue
					r2=get_next_empty_row(temp_board2,enemy_move)
					make_move(temp_board2,enemy,r2,enemy_move)
					if is_winning(temp_board2,enemy):
						moves_value[m]=-1000#if this move make oppenent win give it a worst score
						break
					else:
						moves_value[m]+=50
	print(moves_value)
	return moves_value 



if __name__ == '__main__':
	main(sys.argv[1:])