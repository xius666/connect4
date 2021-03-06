import numpy as np
import pygame
import sys,copy,random
import math
from random import shuffle
from copy import deepcopy

#gloable variable
GREEN = (0,255,0)
WHITE = (255, 255, 250)
RED = (255,0,0)
BLUE = (0,0,255)
SQUARE = 80
HEIGHT = 6
WIDTH = 7
width = WIDTH * SQUARE
height = HEIGHT* SQUARE+SQUARE
size = (width, height)
R = int(SQUARE/2)#radius for circle
HUMAN = 'human'
COMPUTER = 'computer'


def main(argv):
	board = make_board()
	a=is_full(board)
	turn = HUMAN#start with HUMAN player
	pygame.init()
	screen = pygame.display.set_mode(size)
	draw_board(board,screen)
	pygame.display.update()
	if sys.argv[1]=="-AI1":
		play_game(board,screen,sys.argv[1])
	elif sys.argv[1]=="-random":
		play_game(board,screen,sys.argv[1])
	elif sys.argv[1]=="-AI2":
		play_game(board,screen,sys.argv[1])
	elif sys.argv[1]=="-MINI":
		play_game(board,screen,sys.argv[1])
	elif sys.argv[1]=="-player":
		winning=False
		while True :
			if winning or is_full(board):#handle winning case
				if is_full and not winning:
					a =pygame.font.SysFont("arial", 20).render("tie! click screen to replay",False, RED)
					screen.blit(a, (50,10))
				for event in pygame.event.get():
					 # event handling loop
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					elif event.type == pygame.MOUSEBUTTONUP:#click to restart the game
						board = make_board()
						draw_board(board,screen)
						pygame.display.update()
						winning=False
			else:
				# event handling loop
				for event in pygame.event.get():
					dim=(0, 0, width, SQUARE)
					pygame.draw.rect(screen, (0,0,0),dim)
					if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()			
					
					if event.type == pygame.MOUSEMOTION:#when cursor is moved draw the circle!
						x = pygame.mouse.get_pos()[0]#cursor location
						pos=(x,R)
						if turn == HUMAN and winning==False:
							a =pygame.font.SysFont("arial", 15).render("red turn",False, RED)
							screen.blit(a, (20,10))
							pygame.draw.circle(screen, RED, pos, R)
							pygame.display.update()
						else:
							a =pygame.font.SysFont("arial", 15).render("blue turn",False, BLUE)
							screen.blit(a, (20,10))
							pygame.draw.circle(screen, BLUE, pos, R)
							pygame.display.update()

					#Player1 inpput 
					if turn ==HUMAN and event.type == pygame.MOUSEBUTTONUP:
						x = pygame.mouse.get_pos()[0]#cursor location
						col = math.floor(x/SQUARE)#change into column position
						make_move(board, 1, col)#player1 representation is 1
						turn=""
						if is_winning(board, 1):#if player1 wins
							a =pygame.font.SysFont("arial", 20).render("Player 1 wins,click to replay",False, RED)
							screen.blit(a, (150,10))
							winning=True
							turn=HUMAN

					#player2 's turn
					elif turn!=HUMAN and event.type == pygame.MOUSEBUTTONUP:	
						x = pygame.mouse.get_pos()[0]
						col=math.floor(x/SQUARE)			
						make_move(board, 2, col)#player2 representatin is 2
						turn=HUMAN
						if is_winning(board, 2):#if player2 wins
							a =  pygame.font.SysFont("arial", 20).render("player 2 wins,click to replay", False,BLUE)
							screen.blit(a, (150,10))
							winning=True
							turn=HUMAN
					draw_board(board,screen)


def play_game(board,screen,difficulty):
	winning=False
	turn = HUMAN

	while True :
			
			if winning or is_full(board):
				if is_full and not winning:
					a =pygame.font.SysFont("arial", 20).render("tie! click to replay",False, RED)
					screen.blit(a, (50,10))
				for event in pygame.event.get():
					 # event handling loop
					if event.type == pygame.QUIT:
						pygame.quit()

						sys.exit()
					elif turn == HUMAN and event.type == pygame.MOUSEBUTTONUP:#click to restart the game
						board = make_board()
						draw_board(board,screen)
						pygame.display.update()
						winning=False
			else:
				# event handling loop
				for event in pygame.event.get():
					dim=(0, 0, width, SQUARE)
					pygame.draw.rect(screen, (0,0,0),dim)
					if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()		
					if turn == HUMAN and event.type == pygame.MOUSEMOTION:
						a =pygame.font.SysFont("arial", 15).render("your turn",False, RED)
						screen.blit(a, (20,10))
						x = pygame.mouse.get_pos()[0]
						pos=(x,R)
						if winning==False:
							pygame.draw.circle(screen, RED, pos, R)
							pygame.display.update()

					if turn==HUMAN and event.type == pygame.MOUSEBUTTONUP:

						x = pygame.mouse.get_pos()[0]
						col = math.floor(x/SQUARE)
						make_move(board, 1, col)#Human representation is 1
						turn=COMPUTER
						
						if is_winning(board, 1):#if human wins
							a =pygame.font.SysFont("arial", 20).render("Player wins,click to replay", False, RED)
							screen.blit(a, (150,10))
							winning=True
							turn=HUMAN
						draw_board(board,screen)

				#computer's turn
				if turn==COMPUTER:
								
					if difficulty=="-AI1":#AI version 1
						col=getComputerMove1(board)
					elif difficulty=="-AI2":#AI version2 
						col=getComputerMove2(board)
					elif difficulty=="-MINI":#minmax
						col=mini_max(board, 4, 2)[0]
					elif difficulty=="-random":
						col=randomComputer(board)
					if is_valid_move(board, col):
						a =pygame.font.SysFont("arial", 15).render("computer turn",False, BLUE)
						screen.blit(a, (20,10))
						make_move(board, 2, col)#computer representatin is 2

						turn=HUMAN
						if is_winning(board, 2):
							a =  pygame.font.SysFont("arial", 20).render("COMPUTER wins,click to replay", False, BLUE)
							screen.blit(a, (150,10))
							winning=True
							turn=HUMAN

					draw_board(board,screen)




def make_move(board, player_type,col):
	for row in range(HEIGHT):
		if board[row][col] == 0:
			board[row][col] = player_type
			return

def make_board():
	w=WIDTH
	h=HEIGHT
	board_matrix = [[0 for x in range(w)] for y in range(h)]
	
	return board_matrix


def is_full(board):
	for x in range(WIDTH):
		for y in range(HEIGHT):
			if board[y][x] == 0:
				return False
	return True

def is_valid_move(board, col):#check if it is valid move
	# print(col)
	# print(board)
	if col < 0 or col >= WIDTH or board[HEIGHT-1][col] != 0:
		return False
	return True
	 


def is_winning(board, player_type):
	#check for the winning state
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

	# Check diaganols
	for c in range(WIDTH-3):
		for r in range(HEIGHT-3):
			if board[r][c] == player_type and board[r+1][c+1] == player_type and board[r+2][c+2] == player_type and board[r+3][c+3] == player_type:
				return True

	# Check diaganols
	for c in range(WIDTH-3):
		for r in range(3, HEIGHT):
			if board[r][c] == player_type and board[r-1][c+1] == player_type and board[r-2][c+2] == player_type and board[r-3][c+3] == player_type:
				return True

def draw_board(board,screen):#this function was the idea by https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
	for c in range(WIDTH):
		for r in range(HEIGHT):
			pygame.draw.rect(screen, GREEN, (c*SQUARE, (r+1)*SQUARE, SQUARE, SQUARE))

			pygame.draw.circle(screen, WHITE, (int(c*SQUARE+SQUARE/2), int(r*SQUARE+SQUARE+SQUARE/2)), R)
	
	for c in range(WIDTH):
		for r in range(HEIGHT):	

			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), R)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, BLUE, (int(c*SQUARE+SQUARE/2), height-int(r*SQUARE+SQUARE/2)), R)
	
	pygame.display.update()


def legal_moves(board):
        # Return legal moves that for next player.
        legal = []
        for i in range(len(board[0])):
        	if( board[0][i] == 0 ):
        		legal.append(i)
        return legal


def randomComputer(board):#stupid player 
	#reutrn random comupter move
	move=random.randint(0,6)
	return move


def getComputerMove1(board):
	possible_moves = getPossibleMoves1(board, 2)
	bestMoveValue = -10000#initialise value
	bestMoves = []
	for i in range(WIDTH):
		if possible_moves[i] > bestMoveValue and is_valid_move(board,i):
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
		make_move(temp_board,player_type,m)
		if is_winning(temp_board,player_type):#if winning move it gets 10000 score
			moves_value[m]+=10000
			break
		else:#look at other player's counter move 
			if is_full(board):
				moves_value+=10
			for enemy_move in range(WIDTH):
				temp_board2=copy.deepcopy(temp_board)
				if not is_valid_move(temp_board2,enemy_move):
					continue
				make_move(temp_board2,enemy,enemy_move)
				if is_winning(temp_board2,enemy):
					moves_value[m]-=1000#if this move make oppenent win 
					break
				else:
					moves_value[m]+=50
	print(moves_value)
	return moves_value 


#potential move for the AI using the first method that look two steps ahead(haard level difficulty)
def getComputerMove2(board):
	possible_moves = getPossibleMoves2(board, 2)
	bestMoveValue = -10000#initialise value
	bestMoves = []
	for i in range(WIDTH):
		if possible_moves[i] > bestMoveValue and is_valid_move(board,i):
			bestMoveValue = possible_moves[i]
	for i in range(len(possible_moves)):
		if possible_moves[i] == bestMoveValue:
			bestMoves.append(i)
	return random.choice(bestMoves)

def getPossibleMoves2(board, player_type):

	if player_type==1:
		enemy=2
	else:
		enemy=1
	moves_value=np.zeros(WIDTH)
	for m in range(WIDTH):
		temp_board=copy.deepcopy(board)
		if not is_valid_move(board,m):
			continue
		make_move(temp_board,player_type,m)
		if is_winning(temp_board,player_type):#if winning move it gets 10000 score
			moves_value[m]+=10000
			break
		else:#look at other player's counter move 
			if is_full(board):
				moves_value+=10
			for enemy_move in range(WIDTH):
				temp_board2=copy.deepcopy(temp_board)
				if not is_valid_move(temp_board2,enemy_move):
					continue
				make_move(temp_board2,enemy,enemy_move)
				if is_winning(temp_board2,enemy):
					moves_value[m]-=5000#if this move make oppenent win
				else:
					if is_full(temp_board2):
						moves_value[m]+=10
					moves_value[m]+=50
					for move in range(WIDTH):
						temp_board3=copy.deepcopy(temp_board2)
						if not is_valid_move(temp_board3,move):
							continue
						make_move(temp_board3,player_type,move)
						if is_winning(temp_board3,player_type):#if winning move it gets 1000 score
							moves_value[m]+=1000
							break
						else:
							if is_full(temp_board3):
								moves_value[m]+=10
							for enemy_move in range(WIDTH):
								temp_board4=copy.deepcopy(temp_board3)
								if not is_valid_move(temp_board4,enemy_move):
									continue
								make_move(temp_board4,enemy,enemy_move)
								if is_winning(temp_board4,enemy):
									moves_value[m]-=900#if this move make oppenent win 
									break
								else:

									moves_value[m]+=10
	print(moves_value)
	return moves_value 

def mini_max(board, depth, player_type):#almost done not yet there
	valid_moves = []
	for i in range(WIDTH):
		if is_valid_move(board, i):
			valid_moves.append(i)
	shuffle(valid_moves)
	if player_type==1:
		enemy=2
	else:
		enemy=1
	best_score = float("-inf")
	if depth==0 or is_full(board):#recursion stop condition
			if is_winning(board,2):
				return (0,1000000);
			elif is_winning(board,1):
				return (0,-1000000);
			else:
				return (0,50)

	if player_type==2:#computer move
		v=float("-inf")
		best_move = valid_moves[0]
		for move in valid_moves:
			tempBoard=copy.deepcopy(board)
			make_move(tempBoard,2,move)
			# print(temp_board5)
			board_score = mini_max(tempBoard, depth-1,2)[1]
			if board_score> v:
				v = board_score
				best_move = move
		return (best_move,v)

	else:
		v=float("inf")
		best_move = valid_moves[0]
		for move in valid_moves:
			tempBoard=copy.deepcopy(board)
			make_move(tempBoard,1,move)
			# print(temp_board5)
			board_score = mini_max(tempBoard, depth-1,1)[1]
			if board_score> v:
				v = board_score
				best_move = move
		return (best_move,v)


if __name__ == '__main__':
	main(sys.argv[1:])