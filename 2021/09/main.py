import numpy as np

def read_input(filename):
	with open(filename, 'r') as f:
		map = [[int(v) for v in l.strip()] for l in f]
	return np.array(map)

def find_low_spots(map):
	padded_map = np.pad(map, 1, constant_values=np.iinfo(map.dtype).max)
	lowest_neighbor = np.roll(padded_map,  1, 0)
	lowest_neighbor = np.minimum(lowest_neighbor, np.roll(padded_map, -1, 0))
	lowest_neighbor = np.minimum(lowest_neighbor, np.roll(padded_map,  1, 1))
	lowest_neighbor = np.minimum(lowest_neighbor, np.roll(padded_map, -1, 1))
	spots = padded_map < lowest_neighbor
	return spots[1:-1, 1:-1]

def get_sum_risk_level(map, spots):
	return np.sum((map + 1)[spots])

def neighbors(p, map):
	if p[0]+1 < map.shape[0]:
		yield (p[0]+1, p[1])
	if p[0] > 0:
		yield (p[0]-1, p[1])
	if p[1]+1 < map.shape[1]:
		yield (p[0], p[1]+1)
	if p[1] > 0:
		yield (p[0], p[1]-1)

def basin_size(map, spot):
	basin = set()
	basin.add(spot)
	candidates = set()
	for n in neighbors(spot, map):
		candidates.add(n)
	progres = True

	#print("Finding basin for {}".format(spot))
	while progres:
		progres = False
		next_candidates = set()
		while candidates:
			c = candidates.pop()
			value = map[c]
			for n in neighbors(c, map):
				if map[n] < value and n not in basin:
					#print("{} not in map because of {}, basin {}".format(c, n, basin))
					next_candidates.add(c)
					break

			else:
				#print("{} in map".format(c))
				progres = True
				basin.add(c)
				for n in neighbors(c, map):
					if n not in basin and map[n] != 9:
						next_candidates.add(n)
		candidates = next_candidates

	#where = np.zeros(map.shape, dtype=bool)
	#for p in basin:
		#where[p] = True
	#print(where)
	return len(basin)

def find_basins(map, low_spots):
	basin_sizes = []
	for spot in zip(*low_spots.nonzero()):
		basin_sizes.append(basin_size(map, spot))
	biggest_sizes = sorted(basin_sizes)[-3:]
	print(biggest_sizes[0] * biggest_sizes[1] * biggest_sizes[2])

def main(filename):
	map = read_input(filename)
	#print(map)
	low_spots = find_low_spots(map)
	#print(low_spots)
	print(get_sum_risk_level(map, low_spots))
	find_basins(map, low_spots)

import sys
main(sys.argv[1])
