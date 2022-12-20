from collections import defaultdict
from itertools import count

def read_input(filename):
	edges = defaultdict(list)
	with open(filename, 'r') as f:
		for l in f:
			tokens = l.strip().split('-')
			edges[tokens[0]].append(tokens[1])
			if tokens[0] != 'start' and tokens[1] != 'end':
				edges[tokens[1]].append(tokens[0])
	return edges

def enumerate_paths(edges, path=[], node='start'):
	path.append(node)
	if node == 'end':
		yield path
	else:
		for n in edges[node]:
			if n.isupper() or n not in path:
				yield from enumerate_paths(edges, list(path), n)

def enumerate_more_paths(edges, path=[], node='start'):
	path.append(node)
	if node == 'end':
		yield path
	else:
		for n in edges[node]:
			if n.isupper() or n not in path:
				yield from enumerate_more_paths(edges, list(path), n)
			elif n != 'start' and sum(1 for x in path if x == n) == 1:
				yield from enumerate_paths(edges, list(path), n)

def main(filename):
	edges = read_input(filename)
	print(edges)
	print(sum(1 for x in enumerate_paths(edges)))
	print(sum(1 for x in enumerate_more_paths(edges)))

import sys
main(sys.argv[1])
