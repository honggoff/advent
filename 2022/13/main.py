from pprint import pprint
import itertools
import functools


max_elevation = ord('z') - ord('a')

def read_input(filename):
	with open(filename, 'r') as f:
		for line in f:
			first = eval(line)
			second = eval(next(f))
			next(f)
			yield (first, second)


def compare_lists(left, right):
	for l, r in itertools.zip_longest(left, right):
		r = compare_values(l, r)
		if r != 0:
			return r
	return 0

def compare_ints(left, right):
	if left < right:
		return 1
	if left > right:
		return -1
	return 0

def compare_values(left, right):
	if left is None:
		return 1
	if right is None:
		return -1
	if isinstance(left, list):
		if isinstance(right, list):
			return compare_lists(left.copy(), right.copy())
		else:
			return compare_lists(left.copy(), [right])
	else:
		if isinstance(right, list):
			return compare_lists([left], right.copy())
		else:
			return compare_ints(left, right)


def score(result):
	counter = itertools.count(1)
	return sum(c for r, c in zip(result, counter) if r ==1)


def get_packets(pairs):
	return [p for pair in pairs for p in pair]


def get_divider_indices(packets):
	d1 = [[2]]
	d2 = [[6]]

	packets.append(d1)
	packets.append(d2)
	s = sorted(packets, key=functools.cmp_to_key(compare_values), reverse=True)
	return (s.index(d1), s.index(d2))


def score_dividers(indices):
	a, b = indices
	return (a+1) * (b+1)

def main(filename):
	pairs = list(read_input(filename))
	print(score(compare_values(*p) for p in pairs))
	packets = get_packets(pairs)

	print(score_dividers(get_divider_indices(packets)))

if __name__ == "__main__":
	import sys
	main(sys.argv[1])
