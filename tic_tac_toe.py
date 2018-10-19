import copy
import random

def _init_board():
	return [[0,0,0],
		[0,0,0],
		[0,0,0]]


def _available_moves(board):
	if _is_winning_state(board) or _is_losing_state(board):
		return None
	available_moves = []
	for i, row in enumerate(board):
		for j, column in enumerate(row):
			if column == 0:
				available_moves.append((i, j))
	return available_moves


def _state_identifier(board, num):
	columns = {}
	diagonals = {}
	for i, row in enumerate(board):
		if sum(row) == num:
			return True
		for j, column in enumerate(row):
			if j not in columns:
				columns[j] = 0
			columns[j] += column
			if i == j:
				if True not in diagonals:
					diagonals[True] = 0
				diagonals[True] += column
			if i + j == 2:
				if False not in diagonals:
					diagonals[False] = 0
				diagonals[False] += column
	for column in columns.values():
		if column == num:
			return True
	for diagonal in diagonals.values():
		if diagonal == num:
			return True
	return False


def _is_winning_state(board):
	return _state_identifier(board, 3)


def _is_losing_state(board):
	return _state_identifier(board, -3)


cache = {}

def wins_losses(board, player_1_turn):
	if _is_winning_state(board):
		return 1, 0, 0
	if _is_losing_state(board):
		return 0, 1, 0
	board_as_tuple = tuple([ tuple(row) for row in board ])
	cache_key = (board_as_tuple, player_1_turn)
	if cache_key in cache:
		return cache[cache_key]
	available_moves = _available_moves(board)
	if not available_moves:
		return 0, 0, 1

	wins = 0
	losses = 0
	draws = 0
	found_win = False
	found_lost = False

	for i, j in available_moves:
		temp_board = copy.deepcopy(board)
		temp_board[i][j] = 1 if player_1_turn else -1
		w, l, d = wins_losses(temp_board, not player_1_turn)
		wins += w
		losses += l
		draws += d
		if player_1_turn:
			found_win = found_win or (l == 0 and d == 0)
		if not player_1_turn:
			found_lost = found_lost or (w == 0 and d == 0)

	wins = 0 if found_lost else wins
	losses = 0 if found_win else losses
	draws = 0 if found_win or found_lost else draws

	cache[cache_key] = wins, losses, draws
	return cache[cache_key]


def compute_weight(wins, losses, draws, player_1_turn):

	winning_state = wins != 0 and losses == 0 and draws == 0
	losing_state = wins == 0 and losses != 0 and draws == 0

	if player_1_turn:
		if winning_state:
			return 2147483647, wins
		if losing_state:
			return -2147483647, None
	else:
		if winning_state:
			return -2147483647, None
		if losing_state:
			return 2147483647, losses

	return wins - losses if player_1_turn else losses - wins, None


def next_best_move(board, player_1_turn):
	available_moves = _available_moves(board)
	if not available_moves:
		return None
	best_move = None
	max_weight = None
	min_absolute_wins = 2147483647
	for i, j in available_moves:
		temp_board = copy.deepcopy(board)
		temp_board[i][j] = 1 if player_1_turn else -1
		wins, losses, draws = wins_losses(temp_board, not player_1_turn)
		weight, absolute_wins = compute_weight(wins, losses, draws, player_1_turn)
		if not best_move or weight > max_weight or weight == max_weight and min_absolute_wins > absolute_wins:
			best_move = (i, j)
			max_weight = weight
			min_absolute_wins = absolute_wins
	return best_move


def next_random_move(board, player_1_turn):
	available_moves = _available_moves(board)
	if not available_moves:
		return None
	return random.choice(available_moves)


def print_board(board):
	print " --------- "
	for row in board:
		str = "|"
		for column in row:
			if column == -1:
				tok = 'O'
			elif column == 1:
				tok = 'X'
			else:
				tok = ' '
			str += " {} ".format(tok)
		str += "|"
		print str
	print " --------- "


def two_gods_play_game():
	board = _init_board()
	player_1_turn = True
	best_move = next_best_move(board, player_1_turn)
	while best_move:
		board[best_move[0]][best_move[1]] = 1 if player_1_turn else -1
		print_board(board)
		player_1_turn = not player_1_turn
		best_move = next_best_move(board, player_1_turn)


def one_god_one_idiot_play_game(god_start):
	board = _init_board()
	player_1_turn = True
	if god_start:
		best_move = next_best_move(board, player_1_turn)
	else:
		best_move = next_random_move(board, player_1_turn)
	while best_move:
		board[best_move[0]][best_move[1]] = 1 if player_1_turn else -1
		print_board(board)
		player_1_turn = not player_1_turn
		if player_1_turn and god_start or not player_1_turn and not god_start:
			best_move = next_best_move(board, player_1_turn)
		else:
			best_move = next_random_move(board, player_1_turn)


print "\nTWO GODS\n"
two_gods_play_game()
print "\nONE GOD, ONE IDIOT\n"
one_god_one_idiot_play_game(True)
print "\nONE IDIOT, ONE GOD\n"
one_god_one_idiot_play_game(False)

