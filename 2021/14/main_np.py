from collections import Counter
from time import time
import numpy as np

def read_input(filename):
	with open(filename, 'r') as f:
		rules = {}
		template = np.array([ord(c) for c in next(f).strip()])
		for l in f:
			if l.strip():
				tokens = l.strip().split('->')
				fr = tokens[0].strip()
				to = tokens[1].strip()
				index = ord(fr[0]) << 8 | ord(fr[1])
				value = ord(to[0])
				rules[index] = value
		return template, rules

def make_step(polymer, rules):
	new_poly = np.zeros(len(polymer) * 2 - 1, dtype=int)
	first = polymer[0]
	new_poly[0] = first
	i = 1
	for second in polymer[1:]:
		index = first << 8 | second
		new_poly[i] = rules[index]
		i += 1

		new_poly[i] = second
		i += 1
		first = second
	return new_poly

def score(poly):
	c = Counter(poly)
	l = c.most_common()
	return l[0][1] - l[-1][1]
	print(l)

def main(filename):
	polynomial, rules = read_input(filename)
	poly = list(polynomial)
	print(poly, rules)
	start = time()
	steps = 25
	for i in range(steps):
		poly = make_step(poly, rules)

		if i == 9:
			print("Score", score(poly))
		print("step {}, time {}, counts {}".format(i+1, time() - start, Counter(poly)))

	print(score(poly))

import sys
main(sys.argv[1])
