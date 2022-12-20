from collections import deque
from time import time
import numpy as np

def read_input(filename):
	map = []
	with open(filename, 'r') as f:
		for l in f:
			map.append([int(x) for x in l.strip()])
	return np.array(map)

def neighbors(point, map):
	if point[0] > 0:
		yield (point[0]-1, point[1])
	if point[1] > 0:
		yield (point[0], point[1]-1)
	if point[0]+1 < map.shape[0]:
		yield (point[0]+1, point[1])
	if point[1]+1 < map.shape[1]:
		yield (point[0], point[1]+1)

def find_minimal_risk_path(risk):
	cost = np.full(risk.shape, np.iinfo(risk.dtype).max)
	cost[0, 0] = 0
	queue = deque([(0, 0)])
	while queue:
		p = queue.popleft()
		for n in neighbors(p, cost):
			if cost[n] > cost[p] + risk[n]:
				cost[n] = cost[p] + risk[n]
				queue.append(n)
	#print(cost)
	return cost[-1,-1]

def inflate(risk):
	w = risk.shape[0]
	h = risk.shape[1]
	new_risk = np.empty((w*5, h*5), dtype=risk.dtype)
	risks = [risk]
	for i in range(8):
		t = risks[-1]+1
		t[t == 10] = 1
		risks.append(t)

	for x in range(5):
		for y in range(5):
			new_risk[x*w:(x+1)*w, y*h:(y+1)*h] = risks[x+y]
	return new_risk

def main(filename):
	risk = read_input(filename)
	print(risk)
	print(find_minimal_risk_path(risk))

	big_risk = inflate(risk)
	print(find_minimal_risk_path(big_risk))

	np.set_printoptions(linewidth=400, edgeitems=20)
	#print(big_risk)

import sys
main(sys.argv[1])
