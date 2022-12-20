import numpy as np

def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			yield int(line)

def number_increases(depth, filter_size):
	shift = filter_size - 1
	depth_sum = np.zeros(len(depth) - shift)
	if shift == 0:
		shift = - len(depth)
	for i in range(filter_size):
		depth_sum += np.roll(depth, -i)[:-shift]
	#print(depth_sum)

	shifted = np.roll(depth_sum, -1)[:-1]
	return sum(depth_sum[:-1] < shifted)

def main(filename):
	depth = np.array([x for x in read_input(filename)])
	print(number_increases(depth, 1))
	print(number_increases(depth, 3))


import sys
main(sys.argv[1])
