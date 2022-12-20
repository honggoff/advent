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

def calculate_fuel(positions):
	fuel = np.zeros(max(positions), dtype=int)
	for p in range(len(fuel)):
		fuel[p] = np.sum(np.abs(positions - p))
	return fuel

def calculate_expensive_fuel(positions):
	fuel = np.zeros(max(positions), dtype=int)
	for p in range(len(fuel)):
		dist = np.abs(positions - p)
		fuel[p] = np.sum(dist * (dist + 1) / 2)
	return fuel

def main(filename):
	positions = read_input(filename)
	fuel = calculate_fuel(positions)
	print(np.min(fuel))
	fuel = calculate_expensive_fuel(positions)
	print(np.min(fuel))

import sys
main(sys.argv[1])
