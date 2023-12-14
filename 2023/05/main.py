from pprint import pprint
import string
from itertools import islice

def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def read_input(filename):
	with open(filename, 'r') as f:
		line = next(f)
		seeds = [int(s) for s in line.split(':')[1].split()]
		next(f)

		mapping_dest = {}
		mappings = {}
		for line in f:
			mapping = line.split()[0]
			(frm, to) = mapping.split('-to-')
			mapping_dest[frm] = to
			mapping = []
			for line in f:
				if not line.strip():
					break
				dest, src, length = (int(v) for v in line.split())
				mapping.append((dest, src, length))
			mappings[frm] = mapping
		return seeds, mapping_dest, mappings


def do_mapping(value, mapping):
	for (dest, src, length) in mapping:
		if src <= value < src + length:
			return dest + value - src
	return value


def process(seed, mapping_dest, mappings):
	current = 'seed'
	value = seed
	goal = 'location'
	while current != goal:
		value = do_mapping(value, mappings[current])
		current = mapping_dest[current]
	return value


def all_seeds(seed_ranges):
	for (start, count) in batched(seed_ranges, 2):
		next_step = 0
		step = 0
		for s in range(start, start+count):
			if s > next_step:
				step = step + 1
				next_step = start + count * step / 10
				print("{} of {}".format(s-start, count))
			yield s


def main(filename):
	seeds, mapping_dest, mappings = read_input(filename)
	print(seeds)
	pprint(mappings)
	print(min(process(seed, mapping_dest, mappings) for seed in seeds))
	print(min(process(seed, mapping_dest, mappings) for seed in all_seeds(seeds)))


import sys
main(sys.argv[1])
