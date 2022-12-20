import numpy as np

def read_input(filename):
	map = np.zeros((10, 10), dtype=int)
	with open(filename, 'r') as f:
		for i, l in enumerate(f):
			map[i, :] = [int(i) for i in l.strip()]
	return map

def neighbors(p):
	if p[0] < 9:
		if p[1] < 9:
			yield (p[0]+1, p[1]+1)
		if p[1] > 0:
			yield (p[0]+1, p[1]-1)
		yield (p[0]+1, p[1])
	if p[0] > 0:
		if p[1] < 9:
			yield (p[0]-1, p[1]+1)
		if p[1] > 0:
			yield (p[0]-1, p[1]-1)
		yield (p[0]-1, p[1])
	if p[1] < 9:
		yield (p[0], p[1]+1)
	if p[1] > 0:
		yield (p[0], p[1]-1)

def step(map):
	done = False
	number_flashes = 0
	map += 1
	flashed = np.zeros((10, 10), dtype=bool)
	while True:
		flashes = np.logical_and(map > 9, np.logical_not(flashed))
		if not np.any(flashes):
			break
		for flash in zip(*flashes.nonzero()):
			number_flashes += 1
			for n in neighbors(flash):
				map[n] += 1
		flashed = np.logical_or(flashed, flashes)
	map[flashed] = 0
	return number_flashes

def main(filename):
	map = read_input(filename)
	print(map)
	sum = 0
	for i in range(10000):
		s = step(map)
		sum += s
		print(map)
		if i == 100:
			print(sum)
		if s == 100:
			print(i+1)
			break

import sys
main(sys.argv[1])
