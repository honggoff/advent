import numpy as np

def read_input(filename):
	with open(filename, 'r') as f:
		l = next(f)
		return np.array([int(x) for x in l.split(',')])

def sort_generations(fish):
	generations = np.zeros(9, dtype=int)
	for f in fish:
		generations[f] += 1
	return generations

def process_day(generations):
	next_generation = np.roll(generations, -1)
	next_generation[8] = generations[0]
	next_generation[6] += generations[0]
	return next_generation

def main(filename):
	fish = read_input(filename)
	generations = sort_generations(fish)
	for i in range(256):
		if i == 80:
			print(np.sum(generations))
		generations = process_day(generations)
	print(np.sum(generations))

import sys
main(sys.argv[1])
