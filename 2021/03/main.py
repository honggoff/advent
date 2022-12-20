import numpy as np

def read_input(filename):
	result = np.empty(0, dtype=int)
	size = 0
	with open(filename, 'r') as f:
		for line in f:
			result = np.append(result, [int(x) for x in line.strip()])
			if size == 0:
				size = result.shape[0]
	print(result, size)
	return np.reshape(result, (-1, size))

def og_rating(input):
	length, size = input.shape
	candidates = np.full(length, True)
	position = 0
	while np.sum(candidates) > 1:
		sum = np.sum(input[candidates], 0)
		threshold = np.sum(candidates) / 2
		bit = sum[position] >= threshold
		candidates = np.logical_and(candidates, (input[:, position] == bit))
		position += 1

	return to_decimal(input[candidates].reshape(size) == 1)

def co2_rating(input):
	length, size = input.shape
	candidates = np.full(length, True)
	position = 0
	while np.sum(candidates) > 1:
		sum = np.sum(input[candidates], 0)
		threshold = np.sum(candidates) / 2
		bit = sum[position] < threshold
		candidates = np.logical_and(candidates, (input[:, position] == bit))
		position += 1

	return to_decimal(input[candidates].reshape(size) == 1)

def to_decimal(binary):
	#print(binary)
	size = binary.shape[0]
	values = np.array([2 ** x for x in range(size - 1, -1, -1)])
	return np.sum(values[binary])

def main(filename):
	input = read_input(filename)
	sum = np.sum(input, 0)
	length, size = input.shape
	larger = sum > (length / 2.)
	gamma = to_decimal(larger)
	epsilon = to_decimal(np.logical_not(larger))

	#print(input, sum > (length / 2.), gamma, epsilon)
	print(gamma, epsilon)
	print(gamma * epsilon)

	og = og_rating(input)
	co2 = co2_rating(input)
	print(og, co2)
	print(og * co2)


import sys
main(sys.argv[1])
