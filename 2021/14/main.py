from collections import Counter
from time import time
import numpy as np

def read_input(filename):
	rules = {}
	with open(filename, 'r') as f:
		template = next(f).strip()
		for l in f:
			if l.strip():
				tokens = l.strip().split('->')
				rules[tokens[0].strip()] = tokens[1].strip()
	return template, rules

def make_step(polymer, rules):
	new_poly = []
	first = polymer[0]
	new_poly.append(first)
	for second in polymer[1:]:
		pair = first + second
		new_poly.append(rules[pair])
		new_poly.append(second)
		first = second
	return new_poly

def score_poly(c):
	l = c.most_common()
	return l[0][1] - l[-1][1]
	print(l)

def count_for_pair(step, pair, rules, counts, counter):
	next_step = step - 1
	first, second = pair
	pattern = first + second
	#if pair in rules:
	new = rules[pattern]
	counter.update(Counter(new))
	if next_step == 1:
		for p in zip([first, *new], [*new, second]):
			counter.update(counts[p[0]+p[1]])
	else:
		for p in zip([first, *new], [*new, second]):
			count_for_pair(next_step, p, rules, counter)

def count_for_step(step, poly, rules, counts):
	next_step = step
	first = None
	c = Counter(poly)
	for second in poly:
		if first is not None:
			count_for_pair(next_step, (first, second), rules, counts, c)
		first = second
	return c

def make_skip_step_rules(rules, skip):
	def make_skip_steps(p, rules):
		for i in range(skip):
			p = make_step(p, rules)
		return p[1:-1]

	return {p: make_skip_steps(p, rules) for p in rules.keys()}

def count_rules(rules):
	return {p: Counter(v) for p, v in rules.items()}


def main(filename):
	polynomial, rules = read_input(filename)
	poly = list(polynomial)
	print(poly, rules)
	start = time()
	steps = 20
	for i in range(steps):
		poly = make_step(poly, rules)

	print("step {}, time {}, counts {}".format(steps, time() - start, Counter(poly)))
	print("Score", score_poly(Counter(poly)))

	start = time()
	skip_rules = make_skip_step_rules(rules, 20)
	skip_counts = count_rules(skip_rules)
	print(skip_counts)
	counts = count_for_step(2, polynomial, skip_rules, skip_counts)
	print("step {}, time {}, counts {}".format(40, time() - start, counts))

	print(score_poly(counts))

import sys
main(sys.argv[1])
