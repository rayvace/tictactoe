from board.board import Board
from rules.rules import Rules
from ai.ai import ArtificialIntelligence

def print_board(grid):
	print grid[0:3]
	print grid[3:6]
	print grid[6:9]

if __name__ == "__main__":
	starter = raw_input("Pick player 1(1) or 2(2) (Player 1 starts...): ")
	while starter not in ['1', '2']:
		starter = raw_input("Invalid: Pick either 1 or 2: ")

	opponent = raw_input("Do you want to play X(X) or O(O): ")
	while opponent not in ['X', 'O']:
		opponent = raw_input("Invalid: Pick either X or O: ")

	rules = Rules()
	board = Board()
	player = ArtificialIntelligence()

	ai_mark = 'O' if opponent == 'X' else 'X'
	next_play = opponent if starter == '1' else ai_mark
	
	#initialize
	rules.next_play = next_play
	rules.set_board(board)

	player.set_mark(ai_mark)
	player.set_board(board)

	end_game = False
	while not end_game:
		print_board(board.grid)
		mark = rules.get_current_player()

		if mark == ai_mark:
			position = player.next_move()
			print 'Robot plays position %d' % position
			board.add_mark(mark, int(position))
		else:
			position = raw_input("Pick a position to play between 1 and 9: ")
			while position not in [str(x) for x in xrange(1,10)]:
				position = raw_input("Invalid: Pick a number between 1 and 9: ")
				
			valid = board.add_mark(mark, int(position))
			while not valid:
				mark = raw_input("Already taken - pick an open position: ")
				valid = board.add_mark(mark, int(position))

		end_game, result = rules.end_game(position)

	print result

