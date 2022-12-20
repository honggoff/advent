import math
import numpy as np
from collections import Counter
from pprint import pprint

REQUIRED_MATCHES = 12

def list_x_rotations(p):
	x, y, z = p
	yield p
	yield np.vstack((x, -z, y))
	yield np.vstack((x, -y, -z))
	yield np.vstack((x,  z, -y))

def list_yz_rotations(p):
	x, y, z = p
	yield np.vstack(( x,  y,  z))
	yield np.vstack((-y,  x,  z))
	yield np.vstack((-x, -y,  z))
	yield np.vstack(( y, -x,  z))
	yield np.vstack((-z,  y,  x))
	yield np.vstack(( z,  y, -x))

def list_rotations(points):
	for xrot in list_x_rotations(points):
		yield from list_yz_rotations(xrot)

def find_overlap(points1, points2):
	x1, y1, z1 = points1
	for points2_rotated in list_rotations(points2):
		offsets = Counter()
		for p2 in points2_rotated.transpose():
			x2, y2, z2 = p2
			p2_offsets = np.vstack((x1-x2, y1-y2, z1-z2))
			offsets.update(tuple(o) for o in p2_offsets.transpose())
		offset, count = offsets.most_common(1)[0]
		if count >= REQUIRED_MATCHES:
			return offset

def read_input(filename):
	scanners = []
	with open(filename, 'r') as f:
		done = False
		while not done:
			points = []
			header = next(f)
			for line in f:
				line = line.strip()
				if not line:
					break
				points.append(np.array([int(c) for c in line.split(',')]).reshape(3, 1))
			else:
				done = True
			scanners.append(np.hstack(points))

	return scanners

def main(filename):
	pass

def test():
	# explode test cases
	all = set()
	for p in list_rotations((1, 2, 3)):
		all.add(tuple(p.flatten()))

	print(len(all))

	s = read_input('test1')
	print(find_overlap(s[0], s[1]))

import sys
if len(sys.argv) > 1:
	main(sys.argv[1])
else:
	test()
