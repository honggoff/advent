from pprint import pprint
import itertools

def read_input(filename):
	with open(filename, 'r') as f:
		line = next(f)
		directions = line.strip()
		next(f)
		edges={}
		for line in f:
			start, rest = line.strip().split(' = ')
			ends = rest.strip('()').split(', ')
			edges[start] = ends
		return directions, edges


def next_node(current_node, direction, edges):
	if direction == 'L':
		i = 0
	else:
		i = 1
	return edges[current_node][i]


def count_steps(directions, edges):
	current = 'AAA'
	current_dir = itertools.cycle(directions)
	steps = 0
	while current != 'ZZZ':
		d = next(current_dir)
		current = next_node(current, d, edges)
		steps += 1
	return steps


def count_parallel(directions, edges):
	current = [n for n in edges.keys() if n[-1] == 'A']
	current_dir = itertools.cycle(directions)
	steps = 0
	print("Starting at {}".format(current))
	while not all(n[-1] == 'Z' for n in current):
		d = next(current_dir)
		current = [next_node(c, d, edges) for c in current]
		steps += 1
		if any(n[-1] == 'A' for n in current):
			print("After {} steps at {}".format(steps, current))

	return steps


def main(filename):
	directions, edges = list(read_input(filename))
	pprint(directions)
	pprint(edges)
	#print(count_steps(directions, edges))
	print(count_parallel(directions, edges))


import sys
main(sys.argv[1])
