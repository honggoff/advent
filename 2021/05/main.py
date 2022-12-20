import numpy as np

def parse_point(s):
	t = s.split(',')
	return np.array([int(x) for x in t])

def read_input(filename):
	lines = []
	with open(filename, 'r') as f:
		for line in f:
			tokens = line.split()
			lines.append((parse_point(tokens[0]), parse_point(tokens[2])))
	return lines

def get_dimensions(lines):
	return max(max(max(p) for p in l) for l in lines)

def mark_field(lines, size):
	field = np.zeros((size+1, size+1), dtype=int)
	for start, end in lines:
		direction = end - start
		length = np.linalg.norm(direction)
		largest = np.linalg.norm(direction, ord=np.inf)
		#print(start, end)
		#print(direction, length)
		if length == largest:
			step = (direction / length).astype(int)
			#print(start, step, end)
			pos = start
			while any(pos != end):
				field[pos[1], pos[0]] += 1
				pos += step
			field[pos[1], pos[0]] += 1
	return field

def mark_field_diagonal(lines, size):
	field = np.zeros((size+1, size+1), dtype=int)
	for start, end in lines:
		direction = end - start
		length = np.linalg.norm(direction)
		largest = np.linalg.norm(direction, ord=np.inf)
		#print(start, end)
		step = (direction / largest).astype(int)
		print(direction, length, largest, step)
		#print(start, step, end)
		pos = start
		while any(pos != end):
			field[pos[1], pos[0]] += 1
			pos += step
		field[pos[1], pos[0]] += 1
	return field

def main(filename):
	lines = read_input(filename)
	size = get_dimensions(lines)
	#print(lines)
	#field = mark_field(lines, size)
	#print(np.sum(field > 1))
	field = mark_field_diagonal(lines, size)
	print(field)
	print(np.sum(field > 1))

import sys
main(sys.argv[1])
