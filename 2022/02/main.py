import numpy as np

def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield line.split()

def decode_turns(input):
	for o, m in input:
		yield (decode_opponent(o), decode_mine(m))

def decode_opponent(s):
	return ord(s) - ord('A') + 1

def decode_mine(s):
	return ord(s) - ord('X') + 1

def score_shape(o, m):
	return m

def score_outcome(o, m):
	"""
	>>> score_outcome(2, 1)
	0
	>>> score_outcome(1, 2)
	6
	>>> score_outcome(3, 1)
	6
	>>> score_outcome(2, 2)
	3
	"""
	d = (m - o + 1) % 3
	return 3 * d

def score_turn(o, m):
	return score_shape(o, m) + score_outcome(o, m)

def score_game(turns):
	return sum(score_turn(o, m) for o, m in turns)

def get_move(o, r):
	#1 lose
	#2 draw
	#3 win
	return (o + r) % 3 + 1

def score_turn_correctly(o, r):
	m = get_move(o, r)
	return score_shape(o, m) + score_outcome(o, m)

def score_game_correctly(turns):
	return sum(score_turn_correctly(o, m) for o, m in turns)

def main(filename):
	d = [x for x in decode_turns(read_input(filename))]
	print(d)
	print(score_game(d))
	print(score_game_correctly(d))

if __name__ == "__main__":
	import sys
	main(sys.argv[1])
