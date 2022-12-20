import numpy as np

BOARD_SIZE = 5

def read_numbers(f):
	line = next(f)
	return [int(x) for x in line.split(",")]

def read_board(f):
	result = np.empty((BOARD_SIZE, BOARD_SIZE), dtype=int)
	for i in range(BOARD_SIZE):
		line = next(f)
		#print(line)
		result[i,:] = [int(x) for x in line.split()]
	return result

def read_input(filename):
	boards = []
	with open(filename, 'r') as f:
		numbers = read_numbers(f)
		for _ in f:
			boards.append(read_board(f))
	return numbers, boards

def solve_winner(numbers, boards):
	scores = [np.full((BOARD_SIZE, BOARD_SIZE), False)] * len(boards)
	for number in numbers:
		for b in range(len(boards)):
			scores[b] = np.logical_or(scores[b], boards[b] == number)
			if np.max(scores[b].sum(0)) == BOARD_SIZE or \
			   np.max(scores[b].sum(1)) == BOARD_SIZE:
				best = b
				break
		else:
			continue
		break

	points = np.sum(boards[b][np.logical_not(scores[b])])
	print(points, number)
	return points * number

def solve_loser(numbers, boards):
	num_boards = len(boards)
	scores = [np.full((BOARD_SIZE, BOARD_SIZE), False)] * num_boards
	won = np.full(num_boards, False)
	for number in numbers:
		for b in range(num_boards):
			if won[b]:
				continue
			scores[b] = np.logical_or(scores[b], boards[b] == number)
			if np.max(scores[b].sum(0)) == BOARD_SIZE or \
			   np.max(scores[b].sum(1)) == BOARD_SIZE:
				won[b] = True
				if np.sum(won) == num_boards:
					break
		else:
			continue
		break

	points = np.sum(boards[b][np.logical_not(scores[b])])
	print(points, number)
	return points * number

def main(filename):
	numbers, boards = read_input(filename)
	#print(numbers, boards)
	print(solve_winner(numbers, boards))
	print(solve_loser(numbers, boards))

import sys
main(sys.argv[1])
