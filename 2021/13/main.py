import numpy as np
from PIL import Image

def read_input(filename):
	dots = []
	instructions = []
	with open(filename, 'r') as f:
		for l in f:
			if l.strip():
				tokens = l.strip().split(',')
				dots.append((int(tokens[0]), int(tokens[1])))
			else:
				break
		for l in f:
			instruction = l.split()[2].split('=')
			direction = 0 if instruction[0] == 'x' else 1
			instructions.append((direction, int(instruction[1])))
	xmax = max(d[0] for d in dots)
	ymax = max(d[1] for d in dots)
	map = np.zeros((xmax+1, ymax+1), dtype=bool)
	for d in dots:
		map[d] = True
	return map, instructions

def fold(map, instruction):
	axis = instruction[0]
	folded = np.logical_or(map, np.flip(map, axis))
	if axis == 0:
		return folded[0:int(map.shape[0]/2), :]
	return folded[:, 0:int(map.shape[1]/2)]

def main(filename):
	np.set_printoptions(linewidth=200)
	map, instructions = read_input(filename)
	print(map.astype(int).transpose())
	for instruction in instructions:
		map = fold(map, instruction)
		print(np.sum(map))
	print(map.astype(int).transpose())
	i = Image.fromarray(map.transpose())
	i.show()

import sys
main(sys.argv[1])
